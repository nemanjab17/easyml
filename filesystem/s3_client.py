import boto3
from boto3.exceptions import Boto3Error
import uuid
import inject
from database.models import FileRecord
from easyml_util.exceptions import (
    EasyMLBoto3Exception,
    EasyMLSQLAlchemyException,
    ResourceNotFoundException
    )
from sqlalchemy.exc import SQLAlchemyError
from helpers.converters import sqlalch_list_to_json


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

    def download_file(self, file_id):
        pass

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

    def get_file(self, file_id):
        """
        Na osnovu id-a vraca podatke o fajlu.
        :return:
        """
        pass


class FileMapper:

    def __init__(self):
        self.session = inject.instance("dbsession")

    def get_file(self, file_id):
        try:
            return self.session.query(FileRecord).filter(id==file_id).first()
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

    def get_files_of_user(self, user_id):
        try:
            objects = self.session.query(FileRecord).filter(user_id==user_id).all()
            return sqlalch_list_to_json(objects)
        except SQLAlchemyError as e:
            print(e)
            raise EasyMLSQLAlchemyException()

    def add_file(self, file_obj, file_id, user_id):
        try:
            file_record = FileRecord(
                id=file_id,
                filename=file_obj.filename,
                content_type=file_obj.content_type,
                user_id=user_id
                )
            self.session.add(file_record)
        except SQLAlchemyError as e:
            print(e)
            raise EasyMLSQLAlchemyException()

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

    def __init__(self):
        self.s3 = S3Client()
        self.db = FileMapper()

    def get_files_of_user(self, user_id):
        return self.db.get_files_of_user(user_id)

    def save_file(self, file_obj, user_id):
        try:
            file_id = str(uuid.uuid4())
            self.s3.save_file(file_obj, file_id)
            self.db.add_file(file_obj, file_id, user_id)
            self.db.commit()
            return file_id
        except Exception as e:
            print(e)
            self.db.rollback()

    def remove_file(self, file_id):
        self.s3.remove_file(file_id)
        self.db.delete_file(file_id)
        self.db.commit()

    def download_file(self, file_id):
        pass

    def get_file(self, file_id):
        self.db.get_file(file_id)


