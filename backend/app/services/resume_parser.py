\
import fitz


class ResumeParsingError(Exception):
    """Raised when a resume cannot be parsed safely."""


MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
MAX_PAGES = 20


def extract_resume_text(file_bytes: bytes) -> dict:
    if not file_bytes:
        raise ResumeParsingError("The uploaded file is empty.")

    if len(file_bytes) > MAX_FILE_SIZE:
        raise ResumeParsingError("File exceeds the 5 MB upload limit.")

    if not file_bytes.startswith(b"%PDF-"):
        raise ResumeParsingError("The uploaded file is not a valid PDF.")

    try:
        with fitz.open(stream=file_bytes, filetype="pdf") as document:
            if document.is_encrypted:
                raise ResumeParsingError(
                    "Password-protected PDFs are not supported."
                )

            page_count = document.page_count

            if page_count == 0:
                raise ResumeParsingError("The PDF contains no pages.")

            if page_count > MAX_PAGES:
                raise ResumeParsingError(
                    f"PDF exceeds the {MAX_PAGES}-page limit."
                )

            text = "\n".join(
                page.get_text() for page in document
            )

    except ResumeParsingError:
        raise
    except Exception as exc:
        raise ResumeParsingError(
            "Unable to read this PDF. Please upload another file."
        ) from exc

    text = text.strip()

    if not text:
        raise ResumeParsingError(
            "No selectable text was found. This may be a scanned PDF."
        )

    return {
        "text": text,
        "page_count": page_count,
        "character_count": len(text),
    }
