from email.policy import default

import streamlit as st
from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        if hasattr(self, 'document_title'):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, self.document_title, 0, 1, 'C')
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    def chapter_title(self, title, font='Arial', size=12):
        self.set_font(font, 'B', size)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)
    def chapter_body(self, body, font='Arial', size=12):
        self.set_font(font, '', size)
        self.multi_cell(0, 10, body)
        self.ln()

def create_pdf(filename, document_title, author, chapters, image_path=None):
    pdf = PDF()
    pdf.document_title = document_title
    pdf.add_page()
    if author:
        pdf.set_author = author
    if image_path:
        pdf.image(image_path, x=10, y=25, w=pdf.w-20)
        pdf.ln(120)
    for chapter in chapters:
        title, body, font, size = chapter
        pdf.chapter_title(title, font, size)
        pdf.chapter_body(body, font, size)
    pdf.output(filename)

def main():
    st.title('Python PDF Generator')
    st.header('Document configuration')
    document_title=st.text_input('Document title', '...document title')
    author=st.text_input('Author', '...author')
    upload_image=st.file_uploader('Upload an image to the document', type=['jpg', 'jpeg', 'png'])
    st.header('Document chapters')
    chapters=[]
    chapter_count=st.number_input('Chapters quantity', min_value=1, max_value=8, value=1)
    for i in range(chapter_count):
        st.subheader(f'Chapter {i+1}')
        title = st.text_input(f'Chapter {i+1} title', '...')
        body = st.text_area(f'Chapter {i+1} body', '...')
        font = st.selectbox(f'Chapter {i+1} font-type', ['Arial', 'Courier', 'Times'])
        size = st.slider(f'Chapter {i+1} font-size', 8, 12, 24)
        chapters.append((title, body, font, size))

    if st.button('Generate_PDF'):
        image_path=upload_image.name if upload_image else None
        if image_path:
            with open(image_path, 'wb') as f:
                f.write(upload_image.getbuffer())
        create_pdf('output_document_FPDF.pdf', document_title, author, chapters, image_path)
        with open('output_document_FPDF.pdf', 'rb') as pdf_file:
            pdf_bytes=pdf_file.read()
        st.download_button(
            label='Download PDF',
            data=pdf_bytes,
            file_name='output_document_FPDF.pdf',
            mime='application/octet-stream'
        )
        st.success('Successful document creation')

if __name__ == '__main__':
    main()

