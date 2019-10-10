import boto3
from boto3.exceptions import Boto3Error
import uuid
import inject
from database.models import FileRecord
from easyml_util.exceptions import (
    EasyMLBoto3Exception,
    EasyMLSQLAlchemyException,
    ResourceNotFoundException,
    NotProcessableException
    )
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import load_only
from helpers.converters import sqlalch_list_to_json
import pandas as pd

import os


class S3Client:
    """
    S3Client klasa prihvata
    """
    aws_access_key_id = "AKIAJDVPU5LYQXY7XKJA"
    aws_secret_access_key = "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"

    s3_client = boto3.client("s3",
                            aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key)

    s3_resource = boto3.resource("s3",
                               aws_access_key_id=aws_access_key_id,
                               aws_secret_access_key=aws_secret_access_key)
    bucket = "easymlfiles"

    def save_file(self, file_obj, file_id, acl="public-read"):
        try:
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket,
                file_id,
                ExtraArgs={
                    "ACL": acl,
                    "ContentType": file_obj.content_type
                }
            )
        except Boto3Error as e:
            print(e)
            raise EasyMLBoto3Exception()

    def remove_file(self, file_id):
        try:
            obj = self.s3_resource.Object(
                self.bucket,
                str(file_id))
            obj.delete()
        except Boto3Error as e:
            print(e)
            raise EasyMLBoto3Exception()

    def download_file(self, file_id, foler_path):
        # download file from s3 to temp folder
        self.s3_client.download_file(
            self.bucket,
            file_id,
            foler_path
            )


class FileMapper:

    def __init__(self):
        self.session = inject.instance("dbsession")

    def get_file(self, file_id):
        try:
            return self.session.query(FileRecord).filter(FileRecord.id==file_id).first()
        except SQLAlchemyError as e:
            print(e)
            raise EasyMLSQLAlchemyException()

    def delete_file(self, file_id):
        try:
            file_id = str(file_id)
            if self.session.query(FileRecord).filter(FileRecord.id==file_id).delete() == 0:
                print("yesss")
                raise ResourceNotFoundException
        except SQLAlchemyError as e:
            print(e)
            raise EasyMLSQLAlchemyException()

    def get_files_of_user(self, user_id, cols=None):
        try:
            objects = self.session.query(FileRecord).filter(user_id==user_id).all()
            return sqlalch_list_to_json(objects, cols)
        except SQLAlchemyError as e:
            print(e)
            raise EasyMLSQLAlchemyException()

    def add_file(self, file_obj, file_id, user_id, header):
        try:

            file_record = FileRecord(
                id=file_id,
                filename=file_obj.filename,
                content_type=file_obj.content_type,
                user_id=user_id,
                header=header
                )
            self.session.add(file_record)
        except SQLAlchemyError as e:
            print(e)
            raise EasyMLSQLAlchemyException()

    def add_header_metadata(self, file_id, metadata):
        record = self.session.query(FileRecord).filter(FileRecord.id==file_id).first()
        record.header = metadata

    def commit(self):
        try:
            self.session.commit()
        except SQLAlchemyError as e:
            print(e)
            raise EasyMLSQLAlchemyException()

    def rollback(self):
        try:
            self.session.rollback()
        except SQLAlchemyError as e:
            print(e)
            raise EasyMLSQLAlchemyException()


class FileManager:

    temp_folder_path = "uploads"

    def __init__(self):
        self.s3 = S3Client()
        self.db = FileMapper()

    def get_files_of_user(self, user_id, cols=None):
        return self.db.get_files_of_user(user_id, cols)

    def save_file(self, file_obj, user_id, header):
        try:
            file_id = str(uuid.uuid4())
            self.s3.save_file(file_obj, file_id)
            self.db.add_file(file_obj, file_id, user_id, header)
            self.db.commit()

            return file_id
        except Exception as e:
            self.db.rollback()
            raise e

    def remove_file(self, file_id):
        self.s3.remove_file(file_id)
        self.db.delete_file(file_id)
        self.db.commit()

    def download_file(self, file_id):
        pass

    def get_file_header(self, file_id):
        file = self.db.get_file(file_id)
        return file.header

    def add_header_metadata(self, file_id, metadata):
        header = self.get_file_header(file_id)
        if not len(header) == len(metadata.keys()):
            raise NotProcessableException(
                "Meta data parsing failed."
                "Columns do not match the header of the file."
            )
        metadata_cols = list(metadata.keys())
        prev_cols = header if isinstance(header, list) else list(header.keys())
        for i in range(len(prev_cols)):
            if prev_cols[i] != metadata_cols[i]:
                raise NotProcessableException(
                    "Meta data parsing failed."
                    "Columns do not match the header of the file."
                )
        self.db.add_header_metadata(file_id, metadata)
        self.db.commit()
        return metadata
