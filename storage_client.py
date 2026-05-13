import os
import io
from typing import Optional, List
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_BUCKET

class StorageClient:
    def __init__(self):
        if not SUPABASE_URL or not SUPABASE_KEY:
            raise ValueError("Supabase credentials not found. Check .env")
        self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.bucket = SUPABASE_BUCKET

    def upload_file(self, file_bytes: bytes, destination_path: str, content_type: str = "image/jpeg") -> str:
        """Upload a file (bytes) to Supabase Storage."""
        # Supabase Python client expects file-like object or path.
        # We can pass file-like object for bytes.
        try:
            self.client.storage.from_(self.bucket).upload(
                file=file_bytes,
                path=destination_path,
                file_options={"content-type": content_type, "upsert": "true"}
            )
        except Exception as e:
            # If it already exists and upsert fails (sometimes python client is picky)
            self.client.storage.from_(self.bucket).update(
                file=file_bytes,
                path=destination_path,
                file_options={"content-type": content_type, "upsert": "true"}
            )
        return self.get_public_url(destination_path)

    def upload_file_from_path(self, local_path: str, destination_path: str, content_type: str = "image/jpeg") -> str:
        """Upload a file from local disk to Supabase Storage."""
        with open(local_path, "rb") as f:
            file_bytes = f.read()
            self.client.storage.from_(self.bucket).upload(
                file=file_bytes,
                path=destination_path,
                file_options={"content-type": content_type, "upsert": "true"}
            )
        return self.get_public_url(destination_path)

    def upload_text(self, text: str, destination_path: str) -> str:
        """Upload text content to Supabase Storage."""
        text_bytes = text.encode("utf-8")
        self.client.storage.from_(self.bucket).upload(
            file=text_bytes,
            path=destination_path,
            file_options={"content-type": "text/plain", "upsert": "true"}
        )
        return self.get_public_url(destination_path)

    def download_file(self, file_path: str) -> Optional[bytes]:
        """Download file content as bytes."""
        try:
            response = self.client.storage.from_(self.bucket).download(file_path)
            return response
        except Exception:
            return None

    def download_text(self, file_path: str) -> Optional[str]:
        """Download text file content as string."""
        bytes_content = self.download_file(file_path)
        if bytes_content:
            return bytes_content.decode("utf-8")
        return None

    def get_public_url(self, file_path: str) -> str:
        """Get the public URL for a file in the bucket."""
        return self.client.storage.from_(self.bucket).get_public_url(file_path)

    def list_directory(self, folder_path: str) -> List[dict]:
        """List contents of a directory. Returns list of file dicts."""
        # Supabase list expects a path. E.g. 'input_images/product_name'
        if folder_path.endswith('/'):
            folder_path = folder_path[:-1]
        try:
            res = self.client.storage.from_(self.bucket).list(folder_path)
            # The python client returns a list of dictionaries with 'name', 'id', etc.
            return res
        except Exception:
            return []

    def file_exists(self, file_path: str) -> bool:
        """Check if a file exists."""
        folder = os.path.dirname(file_path)
        filename = os.path.basename(file_path)
        files = self.list_directory(folder)
        for f in files:
            if f.get("name") == filename:
                return True
        return False

    def delete_file(self, file_path: str):
        """Delete a specific file."""
        try:
            self.client.storage.from_(self.bucket).remove([file_path])
        except Exception:
            pass

    def delete_directory(self, folder_path: str):
        """Recursively delete all files in a directory."""
        if folder_path.endswith('/'):
            folder_path = folder_path[:-1]
        items = self.list_directory(folder_path)
        files_to_delete = []
        for item in items:
            name = item.get("name", "")
            if not name:
                continue
            child_path = f"{folder_path}/{name}"
            if item.get("id") is None:
                # It's a subfolder — recurse
                self.delete_directory(child_path)
            else:
                files_to_delete.append(child_path)
        if files_to_delete:
            try:
                self.client.storage.from_(self.bucket).remove(files_to_delete)
            except Exception:
                pass

    # ─── High-Level Helpers ──────────────────────────────────────────────

    def list_folders(self, cloud_path: str) -> List[str]:
        """List only subfolder names at a path (id is None = folder)."""
        items = self.list_directory(cloud_path)
        return [i["name"] for i in items if i.get("name") and i.get("id") is None and not i["name"].startswith(".")]

    def list_files(self, cloud_path: str, extensions: tuple = None) -> List[str]:
        """List only file names at a path, optionally filtered by extension."""
        items = self.list_directory(cloud_path)
        result = []
        for i in items:
            name = i.get("name", "")
            if not name or i.get("id") is None or name.startswith("."):
                continue
            if extensions is None or name.lower().endswith(extensions):
                result.append(name)
        return result

    def path_has_content(self, cloud_path: str) -> bool:
        """Check if a cloud path has any children (files or folders)."""
        return len(self.list_directory(cloud_path)) > 0

    def download_image_tuple(self, cloud_path: str):
        """Download image and return (bytes, mime_type) tuple for api_client."""
        img_bytes = self.download_file(cloud_path)
        if not img_bytes:
            return None
        ext = os.path.splitext(cloud_path)[1].lower()
        mime = "image/png" if ext == ".png" else "image/webp" if ext == ".webp" else "image/jpeg"
        return (img_bytes, mime)


# Singleton instance
storage = StorageClient()
