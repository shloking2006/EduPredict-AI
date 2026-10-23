"""
EduPredict AI - Academic Project Report Generator
Builds a professional, comprehensive, editable DOCX project report conforming to:
- Major Chapter Headings: 16pt, Bold, Primary Blue (#1F497D)
- Section Subheadings: 14pt, Bold, Dark Blue (#002060)
- Subsection Headings: 13pt, Bold
- Body Paragraph Text: 12pt, Times New Roman, 1.15 line spacing, Justified
- Proper standard SPPU academic margins (Left 1.25", Right 1.0", Top 1.0", Bottom 1.0")
- Dedicated space and bordered placeholder frames for pasting real live website / dashboard screenshots
- Covers cover page, certificate, acknowledgement, abstract, TOC, and chapters 1-18 matching prompt structure.
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
CHARTS_DIR = os.path.join(PROJECT_ROOT, "charts")

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_table(doc, headers, data, col_widths=None):
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    # Style Header
    hdr_cells = table.rows[0].cells
    for i, header_text in enumerate(headers):
        hdr_cells[i].text = header_text
        set_cell_background(hdr_cells[i], "1F497D")
        set_cell_margins(hdr_cells[i], top=120, bottom=120, left=140, right=140)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.bold = True
            run.font.name = "Times New Roman"
            run.font.size = Pt(11)
            run.font.color.rgb = RGBColor(255, 255, 255)

    # Style Rows
    for r_idx, row_data in enumerate(data):
        row_cells = table.rows[r_idx + 1].cells
        bg_color = "F2F5F8" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, cell_value in enumerate(row_data):
            row_cells[c_idx].text = str(cell_value)
            set_cell_background(row_cells[c_idx], bg_color)
            set_cell_margins(row_cells[c_idx], top=80, bottom=80, left=120, right=120)
            p = row_cells[c_idx].paragraphs[0]
            if c_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for run in p.runs:
                run.font.name = "Times New Roman"
                run.font.size = Pt(10.5)
                run.font.color.rgb = RGBColor(40, 40, 40)

    # Set column widths if provided
    if col_widths:
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = width

    doc.add_paragraph()  # Spacing
    return table

def add_heading_16(doc, text):
    """Major Chapter Headings: 16pt, Bold"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = RGBColor(31, 73, 125)
    return p

def add_heading_14(doc, text):
    """Section Headings: 14pt, Bold"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0, 32, 96)
    return p

def add_heading_13(doc, text):
    """Subsection Headings: 13pt, Bold"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = RGBColor(40, 40, 40)
    return p

def add_body_12(doc, text):
    """Body Paragraph Text: 12pt, Times New Roman, 1.15 line spacing, Justified"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(20, 20, 20)
    return p

def add_bullet_12(doc, bold_prefix, text):
    """Bullet Point: 12pt, Times New Roman"""
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run_b = p.add_run(bold_prefix)
    run_b.font.name = "Times New Roman"
    run_b.font.size = Pt(12)
    run_b.font.bold = True
    run_t = p.add_run(text)
    run_t.font.name = "Times New Roman"
    run_t.font.size = Pt(12)
    return p

def add_figure_image(doc, image_name, caption_text, width=Inches(5.5)):
    img_path = os.path.join(CHARTS_DIR, image_name)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run = p_img.add_run()
        run.add_picture(img_path, width=width)

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(10)
        run_cap = p_cap.add_run(caption_text)
        run_cap.font.name = "Times New Roman"
        run_cap.font.size = Pt(10.5)
        run_cap.font.italic = True
        run_cap.font.bold = True
        run_cap.font.color.rgb = RGBColor(60, 60, 60)

def add_screenshot_placeholder(doc, box_title, instruction_note, figure_caption, height_in_inches=3.0):
    """
    Creates an explicit, bordered screenshot placeholder box with designated space
    for students/evaluators to paste real website/dashboard screenshots.
    """
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.rows[0].cells[0]
    cell.width = Inches(5.8)
    set_cell_background(cell, "FAFAFA")
    set_cell_margins(cell, top=200, bottom=200, left=200, right=200)

    # Add content to the placeholder cell
    p1 = cell.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.space_before = Pt(20)
    p1.paragraph_format.space_after = Pt(6)
    r1 = p1.add_run(f"📷 [{box_title.upper()}]\n")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(12)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(31, 73, 125)

    p2 = cell.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(24)
    r2 = p2.add_run(f"Paste your live browser screenshot here.\n({instruction_note})")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(10.5)
    r2.font.italic = True
    r2.font.color.rgb = RGBColor(120, 120, 120)

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(4)
    p_cap.paragraph_format.space_after = Pt(14)
    rc = p_cap.add_run(figure_caption)
    rc.font.name = "Times New Roman"
    rc.font.size = Pt(10.5)
    rc.font.bold = True
    rc.font.italic = True
    rc.font.color.rgb = RGBColor(50, 50, 50)


def build_formatted_report():
    doc = docx.Document()

    # Set Standard Academic Margins (Left 1.25", Right 1.0", Top 1.0", Bottom 1.0")
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.25)
        s.right_margin = Inches(1.0)

    # ═════════════════════════════════════════════════════════════════
    # COVER PAGE
    # ═════════════════════════════════════════════════════════════════
    p_head = doc.add_paragraph()
    p_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_head.paragraph_format.space_before = Pt(10)
    p_head.paragraph_format.space_after = Pt(6)
    r_h = p_head.add_run("A Mini-Project Report On\n")
    r_h.font.name = "Times New Roman"
    r_h.font.size = Pt(14)
    r_h.font.bold = True

    p_t = doc.add_paragraph()
    p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_t.paragraph_format.space_before = Pt(4)
    p_t.paragraph_format.space_after = Pt(12)
    rt = p_t.add_run("“EduPredict AI — Student Performance Prediction System”\n")
    rt.font.name = "Times New Roman"
    rt.font.size = Pt(18)
    rt.font.bold = True
    rt.font.color.rgb = RGBColor(31, 73, 125)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(6)
    p_sub.paragraph_format.space_after = Pt(10)
    r_sub = p_sub.add_run(
        "Submitted to\n"
        "Savitribai Phule Pune University, Pune\n\n"
        "In partial fulfillment for the award of the Degree of Bachelor of Engineering\n"
        "in\n"
        "Information Technology\n"
        "(AIML Laboratory Assignment No. 12 — SPPU 2024 Pattern)\n"
    )
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(12)

    p_by = doc.add_paragraph()
    p_by.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_by.paragraph_format.space_before = Pt(10)
    p_by.paragraph_format.space_after = Pt(4)
    r_by = p_by.add_run("Submitted By:\n")
    r_by.font.name = "Times New Roman"
    r_by.font.size = Pt(12)
    r_by.font.bold = True

    stud_headers = ["Sr.", "Student Full Name", "Roll No.", "Exam Seat No.", "PRN Number"]
    stud_data = [
        ["1", "Shlok S. Chaudhari", "[Roll No. ]", "[Seat No. ]", "[PRN No. ]"],
        ["2", "[Student Name 2 - Optional]", "[Roll No. ]", "[Seat No. ]", "[PRN No. ]"],
        ["3", "[Student Name 3 - Optional]", "[Roll No. ]", "[Seat No. ]", "[PRN No. ]"],
        ["4", "[Student Name 4 - Optional]", "[Roll No. ]", "[Seat No. ]", "[PRN No. ]"]
    ]
    create_table(doc, stud_headers, stud_data, [Inches(0.5), Inches(2.2), Inches(1.1), Inches(1.2), Inches(1.3)])

    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_guide.paragraph_format.space_before = Pt(12)
    p_guide.paragraph_format.space_after = Pt(4)
    r_g = p_guide.add_run(
        "Under the Guidance of\n"
        "Prof. Ms. A. S. Thorat\n"
        "(Assistant Professor, Department of Information Technology)\n"
    )
    r_g.font.name = "Times New Roman"
    r_g.font.size = Pt(12)
    r_g.font.bold = True

    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(14)
    p_inst.paragraph_format.space_after = Pt(0)
    r_inst = p_inst.add_run(
        "Department of Information Technology\n"
        "STES’s, Smt. Kashibai Navale College of Engineering, Vadgaon (BK), Pune - 411 041\n"
        "Academic Year: 2026–27\n"
    )
    r_inst.font.name = "Times New Roman"
    r_inst.font.size = Pt(12)
    r_inst.font.bold = True

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════
    # CERTIFICATE & APPROVAL
    # ═════════════════════════════════════════════════════════════════
    p_cert_title = doc.add_paragraph()
    p_cert_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert_title.paragraph_format.space_before = Pt(16)
    p_cert_title.paragraph_format.space_after = Pt(14)
    r_ct = p_cert_title.add_run("CERTIFICATE\n")
    r_ct.font.name = "Times New Roman"
    r_ct.font.size = Pt(16)
    r_ct.font.bold = True
    r_ct.font.color.rgb = RGBColor(31, 73, 125)

    cert_text = (
        "This is to certify that the mini-project report entitled “EduPredict AI — Student Performance Prediction System” "
        "being submitted by Shlok S. Chaudhari (Exam Seat No. _____________) and team members is a bonafide record of work carried out "
        "under the supervision and guidance of Prof. Ms. A. S. Thorat in partial fulfillment of the requirements for Third Year (Information Technology) "
        "AIML Laboratory (Assignment No. 12) under the 2024 Course Pattern of Savitribai Phule Pune University, Pune, in the academic year 2026–27.\n\n"
        "The project demonstrates genuine data collection from the UCI Student Performance repository, scikit-learn preprocessing pipeline design, "
        "multi-model classification comparison, hyperparameter optimization, automated unit testing, and deployment of a production-grade Streamlit web application."
    )
    add_body_12(doc, cert_text)

    doc.add_paragraph()
    sig_headers = ["Date & Place", "Guide Signature", "Head of Department"]
    sig_data = [
        ["Date: ____/____/2026\n\nPlace: Pune", "Prof. Ms. A. S. Thorat\nProject Guide\nDept. of IT", "Dr. M. L. Bangare\nHead of Department\nDept. of IT, SKNCOE"]
    ]
    create_table(doc, sig_headers, sig_data, [Inches(1.9), Inches(2.3), Inches(2.3)])

    doc.add_paragraph()
    p_princ = doc.add_paragraph()
    p_princ.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_pr = p_princ.add_run("Dr. A. V. Deshpande\nPrincipal, SKNCOE, Pune\n\n")
    r_pr.font.name = "Times New Roman"
    r_pr.font.size = Pt(11.5)
    r_pr.font.bold = True

    p_exam = doc.add_paragraph()
    p_exam.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_ex = p_exam.add_run("This practical project report has been examined as per the requirements of Savitribai Phule Pune University, Pune at Smt. Kashibai Navale College of Engineering, Pune-41 on ____________________.\n\n")
    r_ex.font.name = "Times New Roman"
    r_ex.font.size = Pt(11.5)

    t_exam = doc.add_table(rows=1, cols=2)
    t_exam.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_exam.rows[0].cells[0].paragraphs[0].text = "Internal Examiner: ____________________\nSignature: ___________________________"
    t_exam.rows[0].cells[1].paragraphs[0].text = "External Examiner: ____________________\nSignature: ___________________________"
    for c in t_exam.rows[0].cells:
        for r in c.paragraphs[0].runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(11.5)
            r.font.bold = True

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════
    # ACKNOWLEDGEMENT
    # ═════════════════════════════════════════════════════════════════
    add_heading_16(doc, "ACKNOWLEDGEMENT")
    ack_text = (
        "I express my profound gratitude and highest respect to my project guide, Prof. Ms. A. S. Thorat, "
        "Department of Information Technology, Smt. Kashibai Navale College of Engineering, Pune. Her insightful technical critiques, "
        "valuable guidance regarding machine learning pipelines, and steadfast encouragement were instrumental in shaping this practical assignment.\n\n"
        "I express my sincere thanks to Dr. M. L. Bangare, Head of the Department of Information Technology, for providing the required computing "
        "infrastructure, laboratory facilities, and an encouraging academic atmosphere that facilitated the smooth execution of this project. "
        "I am equally grateful to our respected Principal, Dr. A. V. Deshpande, for fostering a center of academic excellence and learning.\n\n"
        "I also extend my sincere appreciation to all faculty and technical staff of the Department of Information Technology for their guidance "
        "and support. Finally, I am profoundly indebted to my family and peers for their continuous moral support and motivation throughout this work."
    )
    add_body_12(doc, ack_text)

    p_sig_ack = doc.add_paragraph()
    p_sig_ack.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_sig_ack.paragraph_format.space_before = Pt(24)
    r_sa = p_sig_ack.add_run("Shlok S. Chaudhari\nExam Seat No. [           ]\nTE Information Technology (SPPU 2024 Pattern)")
    r_sa.font.name = "Times New Roman"
    r_sa.font.size = Pt(12)
    r_sa.font.bold = True

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════
    # ABSTRACT
    # ═════════════════════════════════════════════════════════════════
    add_heading_16(doc, "ABSTRACT")
    abs_text1 = (
        "Predicting student academic performance and proactively detecting individuals in need of educational intervention is a vital "
        "application of Educational Data Mining (EDM) and Artificial Intelligence. Early identification allows academic institutions, counselors, "
        "and faculty mentors to deploy targeted pedagogical assistance before terminal examinations occur. This mini-project, entitled "
        "“EduPredict AI — Student Performance Prediction System”, satisfies all curricular competencies mandated by AIML Assignment No. 12 "
        "under the Savitribai Phule Pune University (SPPU) 2024 Pattern for Third Year Information Technology."
    )
    add_body_12(doc, abs_text1)

    abs_text2 = (
        "The project utilizes the benchmark UCI Student Performance dataset (Mathematics course, 395 student records, 33 attributes) to model "
        "multi-dimensional academic trajectories spanning demographic background, family education, study habits, lifestyle, attendance, and "
        "periodic formative grades. The problem is formulated as a three-tier stratified classification task: Low Performance (Final Grade G3 between "
        "0–9, High Risk), Medium Performance (G3 between 10–14, Moderate Risk), and High Performance (G3 between 15–20, Low Risk). To eliminate "
        "data leakage, a scikit-learn ColumnTransformer pipeline combines StandardScaler for numerical features and OneHotEncoder with "
        "handle_unknown='ignore' for categorical variables."
    )
    add_body_12(doc, abs_text2)

    abs_text3 = (
        "Three supervised learning paradigms were trained and empirically evaluated under 5-fold stratified cross-validation: Random Forest "
        "Classifier (CV Accuracy: 85.75% ± 2.06%), Support Vector Machine with RBF kernel (CV Accuracy: 79.10% ± 5.11%), and Gradient Boosting "
        "Classifier (CV Accuracy: 88.92% ± 1.74%). Gradient Boosting was selected as the superior architecture and optimized via GridSearchCV, "
        "achieving a best cross-validation score of 90.19% and an uncompromised test set accuracy of 89.87% (Weighted Precision: 0.8987, Recall: 0.8987, "
        "F1-Score: 0.8987) on the 20% held-out test split (79 samples). The trained pipeline is serialized using Joblib and served through an interactive "
        "Streamlit web dashboard providing real-time inference, risk evaluation, and automated recommendations. The entire codebase is verified by "
        "32 automated unit tests with 100% pass rate."
    )
    add_body_12(doc, abs_text3)

    p_kw = doc.add_paragraph()
    p_kw.paragraph_format.space_before = Pt(8)
    r_kw = p_kw.add_run("Keywords: ")
    r_kw.font.name = "Times New Roman"
    r_kw.font.bold = True
    r_kw.font.size = Pt(12)
    r_kwt = p_kw.add_run("Educational Data Mining, Student Performance Prediction, Scikit-learn Pipeline, Gradient Boosting, Random Forest, Support Vector Machine, Cross-Validation, Streamlit Dashboard, SPPU AIML Assignment 12.")
    r_kwt.font.name = "Times New Roman"
    r_kwt.font.italic = True
    r_kwt.font.size = Pt(12)

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════
    # TABLE OF CONTENTS
    # ═════════════════════════════════════════════════════════════════
    add_heading_16(doc, "TABLE OF CONTENTS")
    add_body_12(doc, "Note: In Microsoft Word, you may update this table of contents or insert an automatic table of contents after final review.")

    toc_headers = ["Section", "Chapter Title", "Page"]
    toc_data = [
        ["-", "Certificate & Approval", "ii"],
        ["-", "Acknowledgement", "iii"],
        ["-", "Abstract", "iv"],
        ["1", "Introduction", "1"],
        ["2", "Problem Statement and Objectives", "2"],
        ["3", "Background and Technology Review", "4"],
        ["4", "Requirements Analysis", "6"],
        ["5", "System Architecture", "8"],
        ["6", "System Design", "10"],
        ["7", "Application Features and Workflow", "12"],
        ["8", "Implementation Details", "14"],
        ["9", "Machine Learning Pipeline & Model Training", "16"],
        ["10", "Testing Methodology", "18"],
        ["11", "Test Results and Discussion", "20"],
        ["12", "Monitoring and Logging", "22"],
        ["13", "Security and Reliability", "24"],
        ["14", "Limitations", "26"],
        ["15", "Future Enhancements", "27"],
        ["16", "Conclusion", "28"],
        ["17", "References", "29"],
        ["18", "Screenshot Evidence (Designated Space for Website Screenshots)", "30"]
    ]
    create_table(doc, toc_headers, toc_data, [Inches(1.0), Inches(4.5), Inches(0.9)])

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════
    # CHAPTER 1: INTRODUCTION
    # ═════════════════════════════════════════════════════════════════
    add_heading_16(doc, "1. Introduction")

    add_heading_14(doc, "1.1 Overview")
    add_body_12(doc,
        "Machine Learning (ML) has emerged as an essential discipline within modern computing, enabling automated systems to discover complex "
        "patterns across structured datasets and generate predictive insights. In the academic sphere, Educational Data Mining (EDM) applies "
        "machine learning techniques to analyze student progression, identify learning bottlenecks, and enhance institutional outcomes. "
        "Educational institutions routinely maintain multi-attribute records encompassing attendance, socio-demographic indicators, study "
        "habits, and interim examination grades. Leveraging these records through predictive models allows faculty to transition from reactive "
        "interventions to proactive academic support."
    )

    add_heading_14(doc, "1.2 Project Overview")
    add_body_12(doc,
        "The project, entitled “EduPredict AI — Student Performance Prediction System”, is an end-to-end machine learning system developed "
        "for Third Year Information Technology under the Savitribai Phule Pune University (SPPU) 2024 Pattern for AIML Assignment No. 12. "
        "The system trains and compares multiple classification models on the authentic UCI Student Performance dataset to categorize students "
        "into discrete academic performance tiers: Low, Medium, and High. In addition to offline model training and cross-validation, the project "
        "features a responsive Streamlit web application that accepts student input, generates real-time predictions, assesses academic risk, "
        "and presents actionable pedagogical recommendations."
    )

    add_heading_14(doc, "1.3 Motivation")
    add_body_12(doc,
        "In traditional academic environments, students who struggle with foundational coursework often remain unnoticed until end-of-semester "
        "examination results are published. At that juncture, opportunities for timely remediation, mentoring, or counseling have elapsed. "
        "Developing a data-driven prediction system provides faculty advisors with an early diagnostic tool. Furthermore, from an engineering "
        "education standpoint, building this project synthesizes vital practical competencies: data ingestion, missing-value handling, categorical "
        "one-hot encoding, pipeline orchestration, multi-model evaluation, hyperparameter tuning, model serialization, unit testing, and web interface development."
    )

    add_heading_14(doc, "1.4 Educational AI Relevance")
    add_body_12(doc,
        "The educational relevance of EduPredict AI lies in demonstrating how machine learning algorithms operate within a human-centered decision "
        "context. The system does not replace faculty judgment; rather, it provides an evidence-based screening mechanism. By coupling raw "
        "statistical predictions with risk tiers (High Risk, Moderate Risk, Low Risk) and specific remedial actions, the application bridges the "
        "gap between abstract algorithmic metrics and actionable educational intervention."
    )

    add_heading_14(doc, "1.5 Report Organization")
    add_body_12(doc,
        "The remainder of this report is organized into seventeen subsequent sections: Section 2 details problem definition and objectives; "
        "Section 3 reviews technologies; Section 4 analyzes requirements; Sections 5 through 7 explain system architecture, design, and user workflow; "
        "Section 8 details implementation; Section 9 documents ML pipelines; Sections 10 through 13 present testing, results, monitoring, and security; "
        "Sections 14 through 16 discuss limitations, future scope, and conclusions; Section 17 provides references; and Section 18 supplies dedicated "
        "spaces with figure captions for inserting real website screenshots."
    )

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════
    # CHAPTER 2: PROBLEM STATEMENT AND OBJECTIVES
    # ═════════════════════════════════════════════════════════════════
    add_heading_16(doc, "2. Problem Statement and Objectives")

    add_heading_14(doc, "2.1 Problem Statement")
    add_body_12(doc,
        "Given a multi-attribute student dataset containing socio-demographic indicators, parental education, study habits, lifestyle behaviors, "
        "and periodic formative grades, develop an automated machine learning system that accurately classifies each student's final academic "
        "performance into discrete tiers (Low, Medium, High) while avoiding data leakage, optimizing model hyperparameters, providing risk-level "
        "assessments, and delivering real-time predictions through an intuitive web application."
    )

    add_heading_14(doc, "2.2 Aim")
    add_body_12(doc,
        "To build, validate, and deploy a machine learning-based Student Performance Prediction System (EduPredict AI) that categorizes academic "
        "achievement and identifies at-risk students for proactive educational support."
    )

    add_heading_14(doc, "2.3 Objectives")
    add_body_12(doc, "The specific technical objectives of this project include:")
    add_bullet_12(doc, "1. Dataset Collection: ", "Acquire the authentic UCI Student Performance dataset (Mathematics course, 395 instances, 33 attributes) and document feature semantics.")
    add_bullet_12(doc, "2. Data Preprocessing: ", "Implement automated data cleaning, missing-value imputation, numerical scaling, and categorical encoding within a leak-free scikit-learn ColumnTransformer pipeline.")
    add_bullet_12(doc, "3. Multi-Model Training: ", "Train and compare at least three candidate algorithms: Random Forest Classifier, Support Vector Classifier (SVC), and Gradient Boosting Classifier using 5-fold stratified cross-validation.")
    add_bullet_12(doc, "4. Hyperparameter Optimization: ", "Tune the superior model using GridSearchCV to identify optimal parameters and prevent overfitting.")
    add_bullet_12(doc, "5. Comprehensive Evaluation: ", "Evaluate test set performance using Overall Accuracy, Weighted Precision, Weighted Recall, Weighted F1-Score, and Confusion Matrix heatmaps.")
    add_bullet_12(doc, "6. Model Persistence & Serving: ", "Serialize the fitted pipeline using Joblib and build an interactive 6-page Streamlit dashboard.")
    add_bullet_12(doc, "7. Automated Testing: ", "Develop and execute automated unit tests (pytest) to verify preprocessing invariants and prediction accuracy.")

    add_heading_14(doc, "2.4 Scope")
    add_body_12(doc,
        "The project scope encompasses offline model training on the UCI Mathematics dataset, cross-validation benchmarking, hyperparameter "
        "optimization, pipeline serialization, automated unit test verification, and local/cloud web deployment via Streamlit. Out of scope for this "
        "initial version are multi-institutional cross-domain generalization, direct integration with commercial campus ERP databases, and "
        "continuous model retraining pipelines."
    )

    add_heading_14(doc, "2.5 Success Criteria")
    add_body_12(doc, "Table 2.1 defines the verified success criteria and corresponding evidence collected during project execution:")

    t_sc_headers = ["ID", "Success Criterion", "Verified Evidence Source"]
    t_sc_data = [
        ["SC-1", "Public/Local web interface accessible via browser", "Streamlit dashboard running on http://localhost:8501"],
        ["SC-2", "Zero data leakage during preprocessing & scaling", "ColumnTransformer fitted strictly inside Pipeline on training split"],
        ["SC-3", "Multi-model benchmarking on real dataset", "5-fold CV comparison across Random Forest, SVM, and Gradient Boosting"],
        ["SC-4", "Systematic hyperparameter optimization executed", "GridSearchCV tuning yielding optimal learning_rate=0.05, max_depth=3"],
        ["SC-5", "Test set classification accuracy exceeds 85%", "Gradient Boosting achieved 89.87% accuracy on 79 held-out test samples"],
        ["SC-6", "Interactive inference produces risk evaluation", "Real-time form predicts category, confidence %, and recommendations"],
        ["SC-7", "Automated unit test suite verifies software quality", "32 pytest unit tests executed with 100% pass rate in 3.16s"]
    ]
    create_table(doc, t_sc_headers, t_sc_data, [Inches(1.0), Inches(3.2), Inches(2.3)])

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════
    # CHAPTER 3: BACKGROUND AND TECHNOLOGY REVIEW
    # ═════════════════════════════════════════════════════════════════
    add_heading_16(doc, "3. Background and Technology Review")

    add_heading_14(doc, "3.1 Educational Data Mining")
    add_body_12(doc,
        "Educational Data Mining (EDM) is an emerging research field concerned with developing methods for exploring unique types of data "
        "originating from educational settings. Prior EDM literature (Cortez and Silva, 2008) established that academic achievement is "
        "governed by multi-factorial dynamics. Formative evaluations (interim grades G1 and G2) provide strong immediate signals, but socio-economic "
        "features such as parental educational attainment and student attendance patterns supply critical contextual nuance."
    )

    add_heading_14(doc, "3.2 Python Programming Runtime")
    add_body_12(doc,
        "Python (version 3.12.4) serves as the core development language for EduPredict AI. Python's rich ecosystem of open-source data science "
        "libraries, standard typing constructs, readable syntax, and extensive documentation make it the preeminent environment for machine "
        "learning engineering."
    )

    add_heading_14(doc, "3.3 Pandas and NumPy")
    add_body_12(doc,
        "Pandas provides high-performance DataFrame data structures for tabular data manipulation, feature indexing, missing-value inspection, "
        "and exploratory statistics. NumPy provides multidimensional array objects and optimized mathematical routines used internally by "
        "scikit-learn during matrix vectorization and scaling operations."
    )

    add_heading_14(doc, "3.4 Scikit-learn Machine Learning Library")
    add_body_12(doc,
        "Scikit-learn is the standard Python library for classical machine learning algorithms. In this project, scikit-learn supplies the "
        "preprocessing classes (StandardScaler, OneHotEncoder, ColumnTransformer), candidate classifiers (RandomForestClassifier, SVC, "
        "GradientBoostingClassifier), model selection utilities (train_test_split, cross_val_score, GridSearchCV), and evaluation metrics "
        "(accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report)."
    )

    add_heading_14(doc, "3.5 Matplotlib and Seaborn")
    add_body_12(doc,
        "Matplotlib provides low-level plotting primitives for chart generation, while Seaborn supplies high-level statistical plotting "
        "interfaces. In this project, Matplotlib and Seaborn render confusion matrix heatmaps, multi-metric model comparison bar charts, "
        "Gini-based feature importance rankings, and distribution histograms."
    )

    add_heading_14(doc, "3.6 Streamlit Web Framework")
    add_body_12(doc,
        "Streamlit is a modern Python framework designed to build interactive web dashboards directly from Python scripts without requiring "
        "manual HTML, CSS, or JavaScript authoring. Streamlit handles responsive client-server communication, form inputs, session caching "
        "(@st.cache_data, @st.cache_resource), and reactive UI state management."
    )

    add_heading_14(doc, "3.7 Joblib Model Serialization")
    add_body_12(doc,
        "Joblib provides efficient serialization and deserialization for Python objects containing large NumPy arrays. Unlike standard pickle, "
        "Joblib optimizes disk I/O when persisting fitted scikit-learn Pipelines, ensuring fast model loading during application startup."
    )

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════
    # CHAPTER 4: REQUIREMENTS ANALYSIS
    # ═════════════════════════════════════════════════════════════════
    add_heading_16(doc, "4. Requirements Analysis")

    add_heading_14(doc, "4.1 Functional Requirements")
    add_body_12(doc, "The system must satisfy the following functional requirements:")
    add_bullet_12(doc, "FR-1: Data Ingestion: ", "Load the raw UCI student-mat.csv dataset using semicolon delimiters without data loss.")
    add_bullet_12(doc, "FR-2: Target Discretization: ", "Convert continuous final grade G3 (0–20) into three discrete performance categories: Low (0–9), Medium (10–14), and High (15–20).")
    add_bullet_12(doc, "FR-3: Automated Preprocessing: ", "Execute numerical standardization and categorical one-hot encoding seamlessly via a unified ColumnTransformer.")
    add_bullet_12(doc, "FR-4: Multi-Model Benchmarking: ", "Train and compute 5-fold cross-validation scores across Random Forest, SVM, and Gradient Boosting.")
    add_bullet_12(doc, "FR-5: Model Optimization: ", "Execute hyperparameter tuning via GridSearchCV on the best cross-validation model.")
    add_bullet_12(doc, "FR-6: Interactive Prediction: ", "Accept user inputs for all 32 student attributes and return predicted performance class, class probabilities, risk assessment, and recommendations.")
    add_bullet_12(doc, "FR-7: Visual Reporting: ", "Render interactive evaluation tables, confusion matrices, and feature importance charts on the web interface.")

    add_heading_14(doc, "4.2 Non-Functional Requirements")
    add_bullet_12(doc, "NFR-1: Usability: ", "The web interface must be clean, structured, and easy to navigate for non-technical educators.")
    add_bullet_12(doc, "NFR-2: Reliability & Determinism: ", "All random seeds (random_state=42) must be fixed to ensure reproducible training splits and model evaluations.")
    add_bullet_12(doc, "NFR-3: Latency: ", "Inference response time for single-student predictions on the Streamlit dashboard must not exceed 200 milliseconds.")
    add_bullet_12(doc, "NFR-4: Maintainability: ", "Codebase must be strictly modular, separating data loading, preprocessing, model training, evaluation, and prediction into dedicated modules.")

    add_heading_14(doc, "4.3 Hardware Requirements")
    add_body_12(doc, "Development and execution require standard personal computing hardware:")
    add_bullet_12(doc, "Processor: ", "Intel Core i3 / AMD Ryzen 3 or higher (2.0 GHz+ multi-core).")
    add_bullet_12(doc, "Random Access Memory (RAM): ", "4 GB minimum; 8 GB recommended for parallel cross-validation.")
    add_bullet_12(doc, "Storage: ", "500 MB free hard disk space for Python runtime, dependencies, charts, and serialized models.")

    add_heading_14(doc, "4.4 Software Requirements")
    add_body_12(doc, "Table 4.1 specifies the software environment utilized for developing and verifying the system:")

    t_sw_headers = ["Software Component", "Version", "Role in Project"]
    t_sw_data = [
        ["Operating System", "Windows 11 Home (64-bit)", "Development host and execution platform"],
        ["Python Runtime", "Python 3.12.4", "Core programming runtime environment"],
        ["Pandas", "2.2.0+", "Tabular data ingestion and cleaning"],
        ["Scikit-learn", "1.4.0+", "Machine learning algorithms and pipelines"],
        ["Matplotlib / Seaborn", "3.8.0+ / 0.13.2", "Statistical visualization and chart generation"],
        ["Streamlit", "1.32.0+", "Web application framework for user dashboard"],
        ["Joblib", "1.3.0+", "Pipeline and model serialization"],
        ["Pytest", "8.1.0+", "Automated unit testing suite"]
    ]
    create_table(doc, t_sw_headers, t_sw_data, [Inches(1.8), Inches(1.5), Inches(3.2)])

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════
    # CHAPTER 5: SYSTEM ARCHITECTURE
    # ═════════════════════════════════════════════════════════════════
    add_heading_16(doc, "5. System Architecture")

    add_heading_14(doc, "5.1 Architecture Overview")
    add_body_12(doc,
        "EduPredict AI is organized as a layered machine learning architecture. The system separates offline data engineering and model "
        "training from online inference and user presentation. The five principal layers include the Data Ingestion Layer, Preprocessing "
        "Pipeline Layer, Model Training & Optimization Engine, Persistence Layer, and Application/Presentation Layer."
    )

    # Conceptual Architecture Block Diagram in Word
    t_arch = doc.add_table(rows=5, cols=1)
    t_arch.alignment = WD_TABLE_ALIGNMENT.CENTER
    arch_steps = [
        "1. DATA LAYER: UCI Student Performance Dataset (student-mat.csv, 395 records, 33 attributes)",
        "2. PREPROCESSING PIPELINE: StandardScaler (15 num) + OneHotEncoder (17 cat) [ColumnTransformer]",
        "3. MODEL TRAINING & COMPARISON: Random Forest vs. SVM vs. Gradient Boosting (5-Fold Stratified CV)",
        "4. MODEL SELECTION & TUNING: GridSearchCV (Optimal: learning_rate=0.05, max_depth=3, n_estimators=100)",
        "5. INFERENCE & SERVING: Joblib Pipeline Serialization -> Streamlit Multi-Page Web Dashboard"
    ]
    for idx, text in enumerate(arch_steps):
        cell = t_arch.rows[idx].cells[0]
        cell.text = text
        set_cell_background(cell, "EBF1F5")
        set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(11)
            r.font.bold = True
            r.font.color.rgb = RGBColor(31, 73, 125)
    doc.add_paragraph()

    p_f51 = doc.add_paragraph("Figure 5.1: Conceptual Architecture of EduPredict AI System")
    p_f51.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_f51.runs[0].font.italic = True
    p_f51.runs[0].font.bold = True
    p_f51.runs[0].font.size = Pt(10.5)

    add_heading_14(doc, "5.2 Request-Response Flow")
    add_body_12(doc,
        "During live inference, the user opens the Streamlit application in a browser and navigates to the 'Predict Performance' tab. "
        "The user populates thirty-two input parameters corresponding to student demographics, study habits, lifestyle, and formative grades. "
        "Upon clicking 'Predict Performance', Streamlit converts inputs into a single-row Pandas DataFrame and dispatches it to "
        "src/predictor.py. The loaded scikit-learn Pipeline automatically standardizes numerical features and one-hot encodes categorical "
        "variables. The fitted Gradient Boosting model computes discrete class predictions and class probability distributions. The predictor "
        "maps the class to an academic risk profile (High, Moderate, Low Risk) and returns tailored recommendations for display."
    )

    add_heading_14(doc, "5.3 Pipeline Boundaries and Leakage Prevention")
    add_body_12(doc,
        "A critical architectural requirement is the strict prevention of data leakage. In conventional, flawed workflows, scalers and encoders "
        "are fit on the entire dataset prior to splitting, leaking test distribution parameters into training. In EduPredict AI, the "
        "ColumnTransformer is embedded inside an sklearn Pipeline. During cross-validation and training, fit() is called strictly on the "
        "training folds. Test instances and new inference records are processed purely via transform(), preserving rigorous separation."
    )

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════
    # CHAPTER 6: SYSTEM DESIGN
    # ═════════════════════════════════════════════════════════════════
    add_heading_16(doc, "6. System Design")

    add_heading_14(doc, "6.1 Modular Software Decomposition")
    add_body_12(doc, "The codebase is organized into modular Python files adhering to clean architecture principles:")
    add_bullet_12(doc, "src/data_loader.py: ", "Handles raw CSV ingestion, metadata dictionaries, and feature attribute documentation.")
    add_bullet_12(doc, "src/preprocessing.py: ", "Contains clean_data(), categorize_grade(), prepare_features_and_target(), and create_preprocessor().")
    add_bullet_12(doc, "src/model_training.py: ", "Defines model dictionaries, creates full pipelines, runs 5-fold cross-validation, and performs GridSearchCV.")
    add_bullet_12(doc, "src/evaluation.py: ", "Computes classification metrics, confusion matrices, and renders comparison charts to charts/.")
    add_bullet_12(doc, "src/predictor.py: ", "Handles model loading via Joblib, student prediction, probability generation, and risk categorization.")
    add_bullet_12(doc, "train_model.py: ", "End-to-end execution script orchestrating ingestion, training, tuning, evaluation, chart saving, and model serialization.")
    add_bullet_12(doc, "app.py: ", "Multi-page interactive Streamlit dashboard.")

    add_heading_14(doc, "6.2 Data Schema and Variable Mapping")
    add_body_12(doc,
        "The input feature space contains 32 attributes. Formative evaluations G1 and G2 reflect continuous scholastic mastery, while variables "
        "such as studytime (weekly study hours), failures (prior academic failures), schoolsup (educational support), and Medu/Fedu (parental education) "
        "capture behavioral and socio-economic support structures."
    )

    add_heading_14(doc, "6.3 Academic Risk Tier Mapping")
    add_body_12(doc, "Table 6.1 defines the systematic mapping from predicted performance category to operational academic risk levels:")

    t_risk_headers = ["Predicted Class", "Grade Range (G3)", "Risk Category", "Intervention Priority", "Automated Advisory Strategy"]
    t_risk_data = [
        ["Low", "0 to 9", "High Risk", "Urgent / Immediate", "Assign faculty mentor, schedule remedial classes, conduct parent-teacher meeting"],
        ["Medium", "10 to 14", "Moderate Risk", "Medium / Advisory", "Encourage peer study groups, clarify doubts during office hours, track attendance"],
        ["High", "15 to 20", "Low Risk", "Low / Encouragement", "Offer advanced project electives, peer tutoring roles, and competitive guidance"]
    ]
    create_table(doc, t_risk_headers, t_risk_data, [Inches(1.0), Inches(1.1), Inches(1.1), Inches(1.4), Inches(2.0)])

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════
    # CHAPTER 7: APPLICATION FEATURES AND WORKFLOW
    # ═════════════════════════════════════════════════════════════════
    add_heading_16(doc, "7. Application Features and Workflow")

    add_heading_14(doc, "7.1 Multi-Page Streamlit Navigation")
    add_body_12(doc, "The Streamlit dashboard (app.py) provides six organized pages accessible via the sidebar navigation:")
    add_bullet_12(doc, "1. 🏠 Home: ", "Displays high-level production metric cards (Best Model: Gradient Boosting, Test Accuracy: 89.87%, F1-Score: 89.87%, Dataset: 395 records), project overview, and methodology summary.")
    add_bullet_12(doc, "2. 🔮 Predict Performance: ", "Presents an intuitive student input form partitioned into Personal Details, Family Background, Study Habits, and Formative Grades (G1, G2). Submitting triggers real-time inference with probability bars and recommendation cards.")
    add_bullet_12(doc, "3. 📊 Model Evaluation: ", "Displays cross-validation summary tables, test set metric tables, best hyperparameter values, and tabs for Model Comparison charts, Confusion Matrices, and Feature Importance.")
    add_bullet_12(doc, "4. 📈 Visualizations: ", "Renders interactive exploratory data analysis charts, including G3 distribution histograms, G1 vs G3 scatter plots, correlation heatmaps, and study time vs grade boxplots.")
    add_bullet_12(doc, "5. 📋 Dataset Overview: ", "Provides dataset statistics, attribute descriptions, interactive table browsing, and descriptive summary statistics.")
    add_bullet_12(doc, "6. ℹ️ About: ", "Summarizes curricular alignment (SPPU AIML Assignment 12), technology stack, citations, and ethical AI advisory disclaimers.")

    add_heading_14(doc, "7.2 User Inference Workflow")
    add_body_12(doc,
        "To perform a prediction, the educator opens http://localhost:8501, selects 'Predict Performance', enters student details, "
        "and clicks 'Predict Performance'. The system instantly displays the predicted class, confidence level (e.g., 91.2% Medium), "
        "and tailored recommendations (e.g., increase weekly study time, schedule mentoring)."
    )

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════
    # CHAPTER 8: IMPLEMENTATION DETAILS
    # ═════════════════════════════════════════════════════════════════
    add_heading_16(doc, "8. Implementation Details")

    add_heading_14(doc, "8.1 Data Preprocessing Implementation")
    add_body_12(doc,
        "In src/preprocessing.py, the create_preprocessor() function returns a scikit-learn ColumnTransformer. StandardScaler standardizes "
        "the 15 numerical features, and OneHotEncoder(handle_unknown='ignore', sparse_output=False) encodes the 17 categorical features into "
        "dense binary indicators. In clean_data(), missing values are safely filled using column median for numerical columns and mode for "
        "categorical attributes, avoiding chained assignment warnings under pandas Copy-on-Write mode."
    )

    add_heading_14(doc, "8.2 Model Training Pipeline Implementation")
    add_body_12(doc,
        "In src/model_training.py, get_models() returns instances of RandomForestClassifier(n_estimators=100, random_state=42), "
        "SVC(kernel='rbf', probability=True, random_state=42), and GradientBoostingClassifier(n_estimators=100, random_state=42). "
        "The create_model_pipeline() helper combines the ColumnTransformer preprocessor and the classifier into a single Pipeline object."
    )

    add_heading_14(doc, "8.3 Model Serialization & Storage Architecture")
    add_body_12(doc,
        "Upon completing training and optimization, train_model.py serializes the best fitted Pipeline directly to "
        "models/best_model.joblib. In addition, model_metadata.joblib and model_metadata.json are created to store cross-validation "
        "scores, test metrics, parameter dictionaries, and feature name lists for dynamic loading by app.py."
    )

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════
    # CHAPTER 9: MACHINE LEARNING PIPELINE & MODEL TRAINING
    # ═════════════════════════════════════════════════════════════════
    add_heading_16(doc, "9. Machine Learning Pipeline & Model Training")

    add_heading_14(doc, "9.1 Training Protocol and Split")
    add_body_12(doc,
        "The cleaned dataset (395 records) is partitioned into an 80% training set (316 samples) and a 20% test set (79 samples) using "
        "stratified sampling (stratify=y) with random_state=42. Stratification ensures that each subset contains exactly 32.9% Low, 48.6% "
        "Medium, and 18.5% High performance instances."
    )

    add_heading_14(doc, "9.2 5-Fold Stratified Cross-Validation Results")
    add_body_12(doc,
        "Table 9.1 documents the exact cross-validation results recorded across candidate models on the 316-sample training set:"
    )

    t_cv_headers = ["Candidate Algorithm", "Fold 1", "Fold 2", "Fold 3", "Fold 4", "Fold 5", "Mean CV Accuracy", "Std. Dev. (sigma)"]
    t_cv_data = [
        ["Random Forest Classifier", "0.8906", "0.8254", "0.8571", "0.8571", "0.8571", "85.75%", "± 2.06%"],
        ["Support Vector Machine (SVC)", "0.8438", "0.7460", "0.8254", "0.8254", "0.7143", "79.10%", "± 5.11%"],
        ["Gradient Boosting Classifier", "0.8906", "0.9206", "0.8730", "0.8730", "0.8889", "88.92%", "± 1.74%"]
    ]
    create_table(doc, t_cv_headers, t_cv_data, [Inches(1.5), Inches(0.7), Inches(0.7), Inches(0.7), Inches(0.7), Inches(0.7), Inches(1.1), Inches(1.0)])

    add_heading_14(doc, "9.3 Hyperparameter Tuning via GridSearchCV")
    add_body_12(doc,
        "Because Gradient Boosting achieved the highest cross-validation score (88.92%) and lowest variance (± 1.74%), it was selected for "
        "hyperparameter optimization. GridSearchCV evaluated 18 parameter combinations across 5 folds (90 total fits) over learning_rate "
        "[0.05, 0.1, 0.2], max_depth [3, 5, 7], and n_estimators [100, 200]. The optimal parameter configuration was identified as "
        "{learning_rate: 0.05, max_depth: 3, n_estimators: 100}, improving cross-validation accuracy to 90.19%."
    )

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════
    # CHAPTER 10: TESTING METHODOLOGY
    # ═════════════════════════════════════════════════════════════════
    add_heading_16(doc, "10. Testing Methodology")

    add_heading_14(doc, "10.1 Automated Unit Testing Architecture")
    add_body_12(doc,
        "Software quality assurance was enforced through an automated unit test suite authored using pytest. The suite is divided into "
        "tests/test_preprocessing.py (15 tests) and tests/test_predictor.py (17 tests), ensuring comprehensive verification of all data transformations "
        "and inference routines."
    )

    add_heading_14(doc, "10.2 Preprocessing Test Cases")
    add_body_12(doc,
        "The preprocessing test suite validates: (1) grade categorization boundary conditions (G3=9 is Low, G3=10 is Medium, G3=14 is Medium, "
        "G3=15 is High); (2) absence of missing values after cleaning; (3) imputation correctness when artificial NaNs are introduced; (4) "
        "preservation of valid G3 grade bounds [0, 20]; (5) exclusion of G3 from feature matrix X; and (6) ColumnTransformer dimensionality "
        "invariance and absence of NaN values after transformation."
    )

    add_heading_14(doc, "10.3 Prediction and Model Invariant Tests")
    add_body_12(doc,
        "The predictor test suite validates: (1) risk level mappings for Low (High Risk), Medium (Moderate Risk), and High (Low Risk); (2) "
        "presence of recommendation strings and descriptive text; (3) model file existence and successful Joblib loading; (4) presence of "
        "predict() and predict_proba() methods; (5) valid return dictionary schema; (6) probability summation to 1.0 (± 0.01); and (7) "
        "accurate inference on synthetic high-performing (G1=18, G2=19 -> High) and struggling (G1=4, G2=3 -> Low) student profiles."
    )

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════
    # CHAPTER 11: TEST RESULTS AND DISCUSSION
    # ═════════════════════════════════════════════════════════════════
    add_heading_16(doc, "11. Test Results and Discussion")

    add_heading_14(doc, "11.1 Test Case Execution Summary")
    add_body_12(doc, "Table 11.1 summarizes the automated pytest execution results across both test modules:")

    t_test_headers = ["Test Module", "Test Focus", "Tests Run", "Passing", "Failing", "Duration", "Result"]
    t_test_data = [
        ["tests/test_preprocessing.py", "Data cleaning, boundary binning, pipeline invariants", "15", "15", "0", "1.42s", "PASSED (100%)"],
        ["tests/test_predictor.py", "Model loading, risk mappings, inference probabilities", "17", "17", "0", "1.74s", "PASSED (100%)"],
        ["Complete Test Suite", "Full system verification", "32", "32", "0", "3.16s", "VERIFIED SUCCESS"]
    ]
    create_table(doc, t_test_headers, t_test_data, [Inches(1.8), Inches(2.0), Inches(0.6), Inches(0.6), Inches(0.6), Inches(0.7), Inches(1.1)])

    add_heading_14(doc, "11.2 Held-Out Test Set Performance")
    add_body_12(doc,
        "Table 11.2 displays the performance metrics evaluated on the 79 held-out test samples (never exposed during model training):"
    )

    t_res_headers = ["Evaluated Model Architecture", "Accuracy", "Weighted Precision", "Weighted Recall", "Weighted F1-Score"]
    t_res_data = [
        ["Random Forest Classifier", "0.8861 (88.61%)", "0.8907 (89.07%)", "0.8861 (88.61%)", "0.8868 (88.68%)"],
        ["Support Vector Machine (SVC)", "0.8228 (82.28%)", "0.8368 (83.68%)", "0.8228 (82.28%)", "0.8197 (81.97%)"],
        ["Gradient Boosting (Default)", "0.8734 (87.34%)", "0.8760 (87.60%)", "0.8734 (87.34%)", "0.8741 (87.41%)"],
        ["Gradient Boosting (Optimized)*", "0.8987 (89.87%)", "0.8987 (89.87%)", "0.8987 (89.87%)", "0.8987 (89.87%)"]
    ]
    create_table(doc, t_res_headers, t_res_data, [Inches(2.3), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.1)])

    add_heading_14(doc, "11.3 Detailed Classification Report for Best Model")
    add_body_12(doc,
        "Table 11.3 details the per-class precision, recall, and F1-score for the optimized Gradient Boosting Classifier on the test set. "
        "The model achieved 100% precision and recall on the High performance class (15/15 correct), 89% on Medium (34/38 correct), and "
        "85% on Low (22/26 correct):"
    )

    t_cr_headers = ["Class Category", "Precision", "Recall", "F1-Score", "Support (Test Count)"]
    t_cr_data = [
        ["Low Performance (Grade 0–9)", "0.85", "0.85", "0.85", "26"],
        ["Medium Performance (Grade 10–14)", "0.89", "0.89", "0.89", "38"],
        ["High Performance (Grade 15–20)", "1.00", "1.00", "1.00", "15"],
        ["Overall Test Accuracy", "-", "-", "0.90 (89.87%)", "79"],
        ["Macro Average", "0.91", "0.91", "0.91", "79"],
        ["Weighted Average", "0.90", "0.90", "0.90", "79"]
    ]
    create_table(doc, t_cr_headers, t_cr_data, [Inches(2.3), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.1)])

    add_heading_14(doc, "11.4 Feature Importance Insights")
    add_body_12(doc,
        "Gini impurity analysis extracted from the Gradient Boosting estimator indicates that formative grades num__G2 and num__G1 represent "
        "the most influential predictors, followed by father's education (num__Fedu), age, weekend alcohol consumption (num__Walc), study time, "
        "and absences. This confirms that prior academic trajectory combined with family background and attendance provides the most reliable "
        "early signal of student performance."
    )

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════
    # CHAPTER 12: MONITORING AND LOGGING
    # ═════════════════════════════════════════════════════════════════
    add_heading_16(doc, "12. Monitoring and Logging")

    add_heading_14(doc, "12.1 Operational Monitoring")
    add_body_12(doc,
        "During execution, Streamlit provides continuous operational monitoring via its built-in server status and healthz endpoint "
        "(http://localhost:8501/healthz). An automated check confirmed HTTP status 200, verifying that the web server process and application "
        "router remain operational."
    )

    add_heading_14(doc, "12.2 Training and Execution Logs")
    add_body_12(doc,
        "Execution logs generated by train_model.py document each pipeline stage sequentially: dataset loading, missing-value check, "
        "feature separation, 5-fold CV fold scores, GridSearchCV fitting progress (90 fits), test evaluation metrics, confusion matrix "
        "generation, and Joblib serialization. In production, these logs enable straightforward auditing and model lineage tracking."
    )

    add_heading_14(doc, "12.3 Monitoring Limitations")
    add_body_12(doc,
        "The current local monitoring configuration does not include distributed telemetry or automated email alerts. In enterprise campus "
        "deployments, integrating Prometheus metrics, Grafana dashboards, or automated error-tracking services (e.g., Sentry) would enhance "
        "observability."
    )

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════
    # CHAPTER 13: SECURITY AND RELIABILITY
    # ═════════════════════════════════════════════════════════════════
    add_heading_16(doc, "13. Security and Reliability")

    add_heading_14(doc, "13.1 Student Data Privacy & Ethical AI")
    add_body_12(doc,
        "Student educational records constitute sensitive personal data. The UCI benchmark dataset is fully anonymized, containing no personal "
        "names, student identification numbers, or residential addresses. In practical campus deployments, student identification must be "
        "pseudonymized using salted cryptographic hashes to comply with data privacy frameworks (e.g., the Digital Personal Data Protection Act)."
    )

    add_heading_14(doc, "13.2 Algorithmic Advisory Disclaimer")
    add_body_12(doc,
        "Predictions generated by EduPredict AI represent statistical estimates derived from historical empirical training data. They do not "
        "constitute deterministic or punitive judgments regarding a student's innate intellectual capacity. Faculty advisors and institutional "
        "mentors must utilize the predictions strictly as early advisory signals to guide supportive, empathetic interventions."
    )

    add_heading_14(doc, "13.3 Input Validation & Defensive Engineering")
    add_body_12(doc,
        "The Streamlit form restricts numerical inputs to valid logical ranges (e.g., age: 15–22, absences: 0–93, grades: 0–20). Furthermore, "
        "the scikit-learn OneHotEncoder is configured with handle_unknown='ignore', preventing runtime crashes if unexpected categorical "
        "values are encountered."
    )

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════
    # CHAPTER 14: LIMITATIONS
    # ═════════════════════════════════════════════════════════════════
    add_heading_16(doc, "14. Limitations")

    add_heading_14(doc, "14.1 Sample Size and Institutional Bias")
    add_body_12(doc,
        "The UCI Student Performance dataset comprises 395 records collected from two secondary schools in Portugal. Consequently, cultural "
        "norms, secondary-school grading conventions, and regional family dynamics may not transfer directly to Indian engineering collegiate "
        "environments without local fine-tuning."
    )

    add_heading_14(doc, "14.2 Formative Evaluation Dominance")
    add_body_12(doc,
        "Feature importance analysis reveals that G1 and G2 exert a dominant influence on the final prediction. In scenarios where interim "
        "assessment scores are unavailable (e.g., predicting outcomes during initial semester enrollment), prediction accuracy will depend "
        "solely on socio-demographic and behavioral features, likely resulting in lower overall precision."
    )

    add_heading_14(doc, "14.3 Self-Reported Attribute Variance")
    add_body_12(doc,
        "Certain survey attributes (e.g., alcohol consumption, free time, study time) are self-reported and may exhibit subjective bias or "
        "social desirability distortion."
    )

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════
    # CHAPTER 15: FUTURE ENHANCEMENTS
    # ═════════════════════════════════════════════════════════════════
    add_heading_16(doc, "15. Future Enhancements")

    add_heading_14(doc, "15.1 Campus ERP and LMS Integration")
    add_body_12(doc,
        "Future iterations can incorporate automated REST API webhooks connecting EduPredict AI directly to institutional Learning Management "
        "Systems (e.g., Moodle, Canvas, Google Classroom) and campus ERP databases, enabling automatic ingestion of attendance and test records."
    )

    add_heading_14(doc, "15.2 Explainable AI (XAI) Integration")
    add_body_12(doc,
        "Incorporating SHAP (Shapley Additive exPlanations) and LIME libraries will allow the application to render individualized explanation "
        "waterfall plots for each student, showing exactly which attributes contributed to their risk categorization."
    )

    add_heading_14(doc, "15.3 Longitudinal Time-Series Tracking")
    add_body_12(doc,
        "Implementing Recurrent Neural Networks (LSTM/GRU) or Temporal Transformers will enable multi-semester trajectory tracking, capturing "
        "dynamic performance shifts across successive academic terms."
    )

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════
    # CHAPTER 16: CONCLUSION
    # ═════════════════════════════════════════════════════════════════
    add_heading_16(doc, "16. Conclusion")
    add_body_12(doc,
        "EduPredict AI — Student Performance Prediction System successfully satisfies all curricular, academic, and practical objectives "
        "mandated by Savitribai Phule Pune University (SPPU) 2024 Pattern for Third Year Information Technology AIML Assignment No. 12.\n\n"
        "The project demonstrated the complete machine learning lifecycle: acquiring and characterizing the genuine UCI Student Performance dataset "
        "(395 records, 33 attributes); constructing a leak-free scikit-learn ColumnTransformer preprocessing pipeline; benchmarking three candidate "
        "classifiers under 5-fold stratified cross-validation (Random Forest: 85.75%, SVM: 79.10%, Gradient Boosting: 88.92%); and optimizing "
        "Gradient Boosting hyperparameters via GridSearchCV to achieve 90.19% cross-validation and 89.87% test accuracy on held-out samples.\n\n"
        "The serialized model is served through a responsive Streamlit web dashboard providing real-time inference, risk categorization, and "
        "personalized recommendations. The entire software architecture is validated by 32 automated unit tests with 100% pass rate, delivering "
        "a reliable, reproducible, and academically sound practical mini-project."
    )

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════
    # CHAPTER 17: REFERENCES
    # ═════════════════════════════════════════════════════════════════
    add_heading_16(doc, "17. References")
    refs = [
        "P. Cortez and A. Silva, “Using Data Mining to Predict Secondary School Student Performance,” in Proc. 5th FUture BUsiness TEChnology Conference (FUBUTEC 2008), Porto, Portugal, pp. 5–12, EUROSIS, ISBN 978-9077381-39-7, 2008.",
        "UCI Machine Learning Repository, “Student Performance Data Set,” School of Information and Computer Sciences, University of California, Irvine, 2014. [Online]. Available: https://archive.ics.uci.edu/ml/datasets/Student+Performance.",
        "F. Pedregosa, G. Varoquaux, A. Gramfort, V. Michel, B. Thirion, O. Grisel, M. Blondel, P. Prettenhofer, R. Weiss, V. Dubourg, J. Vanderplas, A. Passos, D. Cournapeau, M. Brucher, M. Perrot, and E. Duchesnay, “Scikit-learn: Machine Learning in Python,” Journal of Machine Learning Research, vol. 12, pp. 2825–2830, 2011.",
        "W. McKinney, “Data Structures for Statistical Computing in Python,” in Proc. 9th Python in Science Conference (SciPy 2010), pp. 51–56, 2010.",
        "L. Breiman, “Random Forests,” Machine Learning, vol. 45, no. 1, pp. 5–32, 2001.",
        "J. H. Friedman, “Greedy Function Approximation: A Gradient Boosting Machine,” Annals of Statistics, vol. 29, no. 5, pp. 1189–1232, 2001.",
        "C. Cortes and V. Vapnik, “Support-Vector Networks,” Machine Learning, vol. 20, no. 3, pp. 273–297, 1995.",
        "Streamlit Inc., “Streamlit: The fastest way to build and share data apps,” Official Documentation, 2024. [Online]. Available: https://docs.streamlit.io.",
        "Savitribai Phule Pune University (SPPU), “Third Year Information Technology (TE IT) Course Curriculum & Laboratory Manual (2024 Pattern),” Department of Information Technology, Savitribai Phule Pune University, Pune, 2024."
    ]
    for idx, ref in enumerate(refs):
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_before = Pt(3)
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.left_indent = Inches(0.4)
        p_ref.paragraph_format.first_line_indent = Inches(-0.4)
        r_num = p_ref.add_run(f"[{idx+1}] ")
        r_num.font.bold = True
        r_num.font.name = "Times New Roman"
        r_num.font.size = Pt(11)
        r_text = p_ref.add_run(ref)
        r_text.font.name = "Times New Roman"
        r_text.font.size = Pt(11)

    doc.add_page_break()

    # ═════════════════════════════════════════════════════════════════
    # CHAPTER 18: SCREENSHOT EVIDENCE (DESIGNATED SPACES)
    # ═════════════════════════════════════════════════════════════════
    add_heading_16(doc, "18. Screenshot Evidence")
    add_body_12(doc,
        "This section provides dedicated, formatted spaces with figure captions to attach real browser screenshots captured from the live "
        "EduPredict AI Streamlit dashboard (running at http://localhost:8501) and model training outputs. You can directly paste or insert your "
        "actual website screenshots into the designated bordered frames below:"
    )

    # Screenshot 1: Streamlit Home Dashboard
    add_screenshot_placeholder(
        doc,
        box_title="Screenshot 1: Streamlit Application Homepage & Model Metrics",
        instruction_note="Capture the live web browser at http://localhost:8501 showing Best Model, Test Accuracy (89.87%), F1-Score, and Overview cards.",
        figure_caption="Figure 18.1: Live Streamlit Web Dashboard Homepage with Verified Production Performance Metrics"
    )

    # Screenshot 2: Student Input Inference Form
    add_screenshot_placeholder(
        doc,
        box_title="Screenshot 2: Student Input Inference Form (Predict Performance Tab)",
        instruction_note="Capture the input form showing student attributes: School, Demographics, Study Time, Past Failures, and Formative Grades G1 & G2.",
        figure_caption="Figure 18.2: Interactive Student Information Inference Form on Streamlit Interface"
    )

    # Screenshot 3: Real-Time Prediction & Risk Result
    add_screenshot_placeholder(
        doc,
        box_title="Screenshot 3: Prediction Output & Academic Risk Assessment Result",
        instruction_note="Capture the prediction result showing predicted performance class (Low/Medium/High), confidence percentages, and advisory recommendations.",
        figure_caption="Figure 18.3: Real-Time Performance Prediction, Confidence Probabilities, and Academic Risk Assessment"
    )

    # Screenshot 4: Model Evaluation & Comparison Tab
    add_screenshot_placeholder(
        doc,
        box_title="Screenshot 4: Model Evaluation Page & Comparison Charts",
        instruction_note="Capture the 'Model Evaluation' tab displaying Cross-Validation tables, Test Set metric comparison, and the Model Comparison bar chart.",
        figure_caption="Figure 18.4: Model Evaluation Dashboard displaying Cross-Validation and Test Set Performance Comparisons"
    )

    # Screenshot 5: Confusion Matrix & Feature Importance
    add_screenshot_placeholder(
        doc,
        box_title="Screenshot 5: Confusion Matrix Heatmap & Feature Importance Rankings",
        instruction_note="Capture the Confusion Matrix tab (showing 15/15 High, 34/38 Medium, 22/26 Low) and Top 15 Feature Importances chart.",
        figure_caption="Figure 18.5: Confusion Matrix Heatmap and Top 15 Feature Importances Ranked by Gini Impurity Gain"
    )

    # Screenshot 6: Pytest Automated Unit Test Execution Terminal
    add_screenshot_placeholder(
        doc,
        box_title="Screenshot 6: Automated Unit Test Suite Execution in Terminal (Pytest)",
        instruction_note="Capture the terminal/PowerShell window showing 'python -m pytest tests/ -v' with all 32 unit tests passing in 3.16s.",
        figure_caption="Figure 18.6: Terminal Output confirming 32 Automated Unit Tests Passed with 100% Success Rate"
    )

    # Save Document
    target_path = os.path.join(PROJECT_ROOT, "EduPredict_AI_Project_Report_SPPU_AIML12.docx")
    doc.save(target_path)
    print(f"Formatted report with 16/14/12 typography and screenshot spaces generated at: {target_path}")

if __name__ == "__main__":
    build_formatted_report()
