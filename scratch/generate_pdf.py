from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors

def draw_block(c, x, y, width, height, title, color):
    c.setStrokeColor(colors.black)
    c.setLineWidth(2)
    c.setFillColor(color)
    c.roundRect(x, y, width, height, 10, fill=1, stroke=1)
    
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(x + width/2, y + height/2 - 4, title)

def draw_line(c, x1, y1, x2, y2, label=""):
    c.setStrokeColor(colors.grey)
    c.setLineWidth(2)
    c.line(x1, y1, x2, y2)
    
    # draw arrow head roughly
    if y1 > y2 and x1 == x2: # pointing down
        c.polygon([x2, y2, x2-5, y2+10, x2+5, y2+10], fill=1, stroke=0)
    elif x1 < x2 and y1 == y2: # pointing right
        c.polygon([x2, y2, x2-10, y2-5, x2-10, y2+5], fill=1, stroke=0)
    elif x1 > x2 and y1 == y2: # pointing left
        c.polygon([x2, y2, x2+10, y2-5, x2+10, y2+5], fill=1, stroke=0)
        
    if label:
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 10)
        mid_x = (x1 + x2)/2
        mid_y = (y1 + y2)/2
        c.drawString(mid_x + 5, mid_y + 5, label)

def generate_diagram(filename):
    c = canvas.Canvas(filename, pagesize=landscape(A4))
    width, height = landscape(A4)
    
    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width/2, height - 50, "FAQ Chatbot MPOnline - System Architecture")
    
    bw = 160 # block width
    bh = 50  # block height

    # Center coordinates
    cx = width / 2
    
    # Define block positions (x, y) starting from top center
    pos_user = (cx - bw/2, height - 120)
    pos_frontend = (cx - bw/2, height - 220)
    pos_backend = (cx - bw/2, height - 340)
    
    pos_mongo = (cx + 180, height - 340)
    
    pos_fs = (cx - 280, height - 480)
    pos_ocr = (cx - bw/2, height - 480)
    pos_rag = (cx + 180, height - 480)
    
    pos_gemini = (cx + 180, height - 600) # Below RAG
    
    # Draw Lines
    # User -> Frontend
    draw_line(c, cx, pos_user[1], cx, pos_frontend[1] + bh, "Interacts")
    # Frontend -> Backend
    draw_line(c, cx, pos_frontend[1], cx, pos_backend[1] + bh, "REST API")
    
    # Backend -> MongoDB
    draw_line(c, pos_backend[0] + bw, pos_backend[1] + bh/2, pos_mongo[0], pos_mongo[1] + bh/2, "CRUD")
    
    # Backend -> FS
    draw_line(c, cx, pos_backend[1], pos_fs[0] + bw/2, pos_fs[1] + bh, "Store/Load")
    
    # Backend -> OCR
    draw_line(c, cx, pos_backend[1], pos_ocr[0] + bw/2, pos_ocr[1] + bh, "Extract Text")
    
    # Backend -> RAG
    draw_line(c, pos_backend[0] + bw, pos_backend[1] + bh/4, pos_rag[0] + bw/2, pos_rag[1] + bh, "Query/Ingest")
    
    # RAG -> Gemini
    draw_line(c, pos_rag[0] + bw/2, pos_rag[1], pos_gemini[0] + bw/2, pos_gemini[1] + bh, "Embeddings / LLM")

    # Draw Blocks
    draw_block(c, *pos_user, bw, bh, "User", colors.lightblue)
    draw_block(c, *pos_frontend, bw, bh, "React Web App (Vite)", colors.lightgreen)
    draw_block(c, *pos_backend, bw, bh, "FastAPI Backend", colors.lightcoral)
    draw_block(c, *pos_mongo, bw, bh, "MongoDB Server", colors.lightgrey)
    
    draw_block(c, *pos_fs, bw, bh, "Local File System", colors.wheat)
    draw_block(c, *pos_ocr, bw, bh, "Tesseract OCR Engine", colors.lavender)
    draw_block(c, *pos_rag, bw, bh, "RAG Pipeline (Local)", colors.aquamarine)
    
    draw_block(c, *pos_gemini, bw, bh, "Gemini API", colors.lightpink)
    
    c.save()

if __name__ == "__main__":
    generate_diagram("System_Architecture_Block_Diagram.pdf")
    print("PDF generated successfully.")
