import asyncio
import traceback
from io import BytesIO
from PIL import Image

from app.database import SessionLocal
from app.models.entities import User, UserRole
from app.services.document_service import ingest_document
from fastapi import UploadFile
from starlette.datastructures import Headers

async def main():
    try:
        db = SessionLocal()
        user = db.query(User).filter(User.role == UserRole.ADMIN).first()

        # Create a simple valid image with no actual text
        # But this will trigger Tesseract
        img = Image.new('RGB', (100, 100), color = 'white')
        bytes_io = BytesIO()
        img.save(bytes_io, format='PNG')
        file_content = bytes_io.getvalue()

        upload_file = UploadFile(filename='test.png', file=BytesIO(file_content), size=len(file_content), headers=Headers())
        
        print("Starting ingest_document for PNG...")
        doc = ingest_document(db, upload_file, user)
        print('SUCCESS:', doc.id)
    except Exception as e:
        print("UPLOAD FAILED WITH EXCEPTION:")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
