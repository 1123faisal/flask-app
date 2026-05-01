const {
  Document,
  Packer,
  Paragraph,
  TextRun,
  Table,
  TableRow,
  TableCell,
  AlignmentType,
  BorderStyle,
  WidthType,
  ShadingType,
  HeadingLevel,
  VerticalAlign,
  LevelFormat,
  Header,
  Footer,
  PageNumber,
  TabStopType,
  TabStopPosition,
  UnderlineType,
} = require("docx");
const fs = require("fs");

const BRAND = "003366";
const LIGHT_BLUE = "D5E8F0";
const HEADER_BG = "003366";
const ROW_ALT = "EBF4FA";
const WHITE = "FFFFFF";
const DARK_TEXT = "1A1A2E";
const MID_TEXT = "444466";

const border = { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" };
const borders = { top: border, bottom: border, left: border, right: border };
const noBorder = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };

const cellMargins = { top: 100, bottom: 100, left: 140, right: 140 };
const tightMargins = { top: 60, bottom: 60, left: 140, right: 140 };

function spacer(pts = 120) {
  return new Paragraph({ spacing: { before: 0, after: pts }, children: [new TextRun("")] });
}

function sectionHeading(text) {
  return new Paragraph({
    spacing: { before: 240, after: 100 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: BRAND, space: 4 } },
    children: [new TextRun({ text, bold: true, size: 26, color: BRAND, font: "Arial" })],
  });
}

function label(text) {
  return new TextRun({ text, bold: true, size: 20, color: DARK_TEXT, font: "Arial" });
}

function val(text) {
  return new TextRun({ text, size: 20, color: MID_TEXT, font: "Arial" });
}

// ── HEADER TABLE (company info + title) ──────────────────────────────────────
const headerTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [5200, 4160],
  rows: [
    new TableRow({
      children: [
        new TableCell({
          borders: noBorders,
          margins: { top: 0, bottom: 0, left: 0, right: 0 },
          shading: { fill: HEADER_BG, type: ShadingType.CLEAR },
          verticalAlign: VerticalAlign.CENTER,
          width: { size: 5200, type: WidthType.DXA },
          children: [
            new Paragraph({
              spacing: { before: 160, after: 40 },
              children: [new TextRun({ text: "YOUR COMPANY NAME", bold: true, size: 36, color: WHITE, font: "Arial" })],
            }),
            new Paragraph({
              spacing: { before: 0, after: 40 },
              children: [
                new TextRun({ text: "Software Development Services", size: 20, color: "AACCEE", font: "Arial" }),
              ],
            }),
            new Paragraph({
              spacing: { before: 0, after: 40 },
              children: [
                new TextRun({
                  text: "info@yourcompany.com  |  +91-XXXXXXXXXX",
                  size: 18,
                  color: "AACCEE",
                  font: "Arial",
                }),
              ],
            }),
            new Paragraph({
              spacing: { before: 0, after: 160 },
              children: [new TextRun({ text: "www.yourcompany.com", size: 18, color: "AACCEE", font: "Arial" })],
            }),
          ],
        }),
        new TableCell({
          borders: noBorders,
          margins: { top: 0, bottom: 0, left: 0, right: 0 },
          shading: { fill: HEADER_BG, type: ShadingType.CLEAR },
          verticalAlign: VerticalAlign.CENTER,
          width: { size: 4160, type: WidthType.DXA },
          children: [
            new Paragraph({
              alignment: AlignmentType.RIGHT,
              spacing: { before: 160, after: 60 },
              children: [new TextRun({ text: "QUOTATION", bold: true, size: 52, color: WHITE, font: "Arial" })],
            }),
            new Paragraph({
              alignment: AlignmentType.RIGHT,
              spacing: { before: 0, after: 60 },
              children: [new TextRun({ text: "Quote No: QT-2025-0042", size: 20, color: "AACCEE", font: "Arial" })],
            }),
            new Paragraph({
              alignment: AlignmentType.RIGHT,
              spacing: { before: 0, after: 60 },
              children: [new TextRun({ text: "Date: 27 April 2025", size: 20, color: "AACCEE", font: "Arial" })],
            }),
            new Paragraph({
              alignment: AlignmentType.RIGHT,
              spacing: { before: 0, after: 160 },
              children: [new TextRun({ text: "Valid Until: 27 May 2025", size: 20, color: "AACCEE", font: "Arial" })],
            }),
          ],
        }),
      ],
    }),
  ],
});

// ── CLIENT INFO TABLE ─────────────────────────────────────────────────────────
const clientTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [4600, 4760],
  rows: [
    new TableRow({
      children: [
        new TableCell({
          borders: noBorders,
          shading: { fill: ROW_ALT, type: ShadingType.CLEAR },
          margins: cellMargins,
          width: { size: 4600, type: WidthType.DXA },
          children: [
            new Paragraph({
              spacing: { before: 40, after: 60 },
              children: [new TextRun({ text: "BILL TO", bold: true, size: 18, color: BRAND, font: "Arial" })],
            }),
            new Paragraph({
              spacing: { before: 0, after: 30 },
              children: [
                new TextRun({
                  text: "BluDoc Healthcare Pvt. Ltd.",
                  bold: true,
                  size: 22,
                  color: DARK_TEXT,
                  font: "Arial",
                }),
              ],
            }),
            new Paragraph({
              spacing: { before: 0, after: 30 },
              children: [new TextRun({ text: "Attn: [Client Name]", size: 20, color: MID_TEXT, font: "Arial" })],
            }),
            new Paragraph({
              spacing: { before: 0, after: 30 },
              children: [
                new TextRun({ text: "[Client Address, City, State - PIN]", size: 20, color: MID_TEXT, font: "Arial" }),
              ],
            }),
            new Paragraph({
              spacing: { before: 0, after: 60 },
              children: [
                new TextRun({ text: "GST No: [GSTIN if applicable]", size: 20, color: MID_TEXT, font: "Arial" }),
              ],
            }),
          ],
        }),
        new TableCell({
          borders: noBorders,
          shading: { fill: WHITE, type: ShadingType.CLEAR },
          margins: cellMargins,
          width: { size: 4760, type: WidthType.DXA },
          children: [
            new Paragraph({
              spacing: { before: 40, after: 60 },
              children: [new TextRun({ text: "PROJECT DETAILS", bold: true, size: 18, color: BRAND, font: "Arial" })],
            }),
            new Paragraph({
              spacing: { before: 0, after: 30 },
              children: [label("Project: "), val("BluDoc Patient App — Backend API")],
            }),
            new Paragraph({
              spacing: { before: 0, after: 30 },
              children: [label("Platform: "), val("Node.js REST API")],
            }),
            new Paragraph({ spacing: { before: 0, after: 30 }, children: [label("Rate: "), val("₹1,000 per hour")] }),
            new Paragraph({ spacing: { before: 0, after: 30 }, children: [label("Timeline: "), val("10–16 weeks")] }),
            new Paragraph({
              spacing: { before: 0, after: 60 },
              children: [label("Delivery Mode: "), val("Agile sprints, 2-week cycles")],
            }),
          ],
        }),
      ],
    }),
  ],
});

// ── SCOPE TABLE ───────────────────────────────────────────────────────────────
function makeHeaderRow(cols, widths) {
  return new TableRow({
    tableHeader: true,
    children: cols.map(
      (text, i) =>
        new TableCell({
          borders,
          width: { size: widths[i], type: WidthType.DXA },
          shading: { fill: HEADER_BG, type: ShadingType.CLEAR },
          margins: tightMargins,
          verticalAlign: VerticalAlign.CENTER,
          children: [
            new Paragraph({
              alignment: i > 1 ? AlignmentType.CENTER : AlignmentType.LEFT,
              children: [new TextRun({ text, bold: true, size: 19, color: WHITE, font: "Arial" })],
            }),
          ],
        })
    ),
  });
}

function makeRow(cells, widths, shade) {
  return new TableRow({
    children: cells.map(
      (text, i) =>
        new TableCell({
          borders,
          width: { size: widths[i], type: WidthType.DXA },
          shading: { fill: shade, type: ShadingType.CLEAR },
          margins: tightMargins,
          verticalAlign: VerticalAlign.CENTER,
          children: [
            new Paragraph({
              alignment: i > 1 ? AlignmentType.CENTER : AlignmentType.LEFT,
              children: [
                new TextRun({ text, size: 19, color: i === 4 ? "1A6B35" : DARK_TEXT, bold: i === 4, font: "Arial" }),
              ],
            }),
          ],
        })
    ),
  });
}

const COL_W = [400, 3100, 900, 900, 1260, 800];
const COL_TOTAL = COL_W.reduce((a, b) => a + b, 0); // 7360 — we'll use 9360 split differently

// Adjust columns to fit 9360
const SCOPE_COLS = [480, 3560, 1000, 1000, 1320, 2000];
const SCOPE_TOTAL = SCOPE_COLS.reduce((a, b) => a + b, 0); // 9360

const scopeData = [
  [
    "1",
    "Document Sending API\n(Prescriptions, Certificates, Invoices, Consent, Instructions)",
    "80",
    "120",
    "₹1,000",
    "₹80,000 – ₹1,20,000",
  ],
  [
    "2",
    "Messaging & Communication API\n(Appointments, Reminders, Greetings, Announcements, Offers, SMS)",
    "70",
    "100",
    "₹1,000",
    "₹70,000 – ₹1,00,000",
  ],
  ["3", "Blogs & Content Publishing API", "40", "60", "₹1,000", "₹40,000 – ₹60,000"],
  ["4", "White-Label / Branded App Config API", "30", "50", "₹1,000", "₹30,000 – ₹50,000"],
  [
    "5",
    "Multi-Doctor Account Management API\n(RBAC, Clinic hierarchy, multi-specialty)",
    "50",
    "80",
    "₹1,000",
    "₹50,000 – ₹80,000",
  ],
  [
    "6",
    "Setup, DevOps, QA & Documentation\n(CI/CD, Swagger docs, Testing, Deployment)",
    "70",
    "100",
    "₹1,000",
    "₹70,000 – ₹1,00,000",
  ],
];

const scopeRows = scopeData.map((row, idx) => {
  const shade = idx % 2 === 0 ? WHITE : ROW_ALT;
  return new TableRow({
    children: row.map(
      (text, i) =>
        new TableCell({
          borders,
          width: { size: SCOPE_COLS[i], type: WidthType.DXA },
          shading: { fill: shade, type: ShadingType.CLEAR },
          margins: tightMargins,
          verticalAlign: VerticalAlign.TOP,
          children: text.split("\n").map(
            (line, li) =>
              new Paragraph({
                spacing: { before: li === 0 ? 0 : 40, after: 0 },
                alignment: i > 3 ? AlignmentType.CENTER : AlignmentType.LEFT,
                children: [
                  new TextRun({
                    text: line,
                    size: i === 5 ? 20 : 19,
                    bold: i === 5,
                    color: i === 5 ? "1A6B35" : i === 1 && li === 0 ? DARK_TEXT : MID_TEXT,
                    font: "Arial",
                  }),
                ],
              })
          ),
        })
    ),
  });
});

// Total row
const totalRow = new TableRow({
  children: [
    new TableCell({
      borders,
      columnSpan: 5,
      width: { size: SCOPE_COLS.slice(0, 5).reduce((a, b) => a + b, 0), type: WidthType.DXA },
      shading: { fill: HEADER_BG, type: ShadingType.CLEAR },
      margins: tightMargins,
      children: [
        new Paragraph({
          alignment: AlignmentType.RIGHT,
          children: [
            new TextRun({ text: "TOTAL ESTIMATED PROJECT COST", bold: true, size: 20, color: WHITE, font: "Arial" }),
          ],
        }),
      ],
    }),
    new TableCell({
      borders,
      width: { size: SCOPE_COLS[5], type: WidthType.DXA },
      shading: { fill: "1A6B35", type: ShadingType.CLEAR },
      margins: tightMargins,
      children: [
        new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "₹3,40,000 – ₹5,60,000", bold: true, size: 20, color: WHITE, font: "Arial" })],
        }),
      ],
    }),
  ],
});

const scopeTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: SCOPE_COLS,
  rows: [
    makeHeaderRow(["#", "Module / Deliverable", "Min Hrs", "Max Hrs", "Rate/Hr", "Estimated Cost"], SCOPE_COLS),
    ...scopeRows,
    totalRow,
  ],
});

// ── TECH STACK TABLE ──────────────────────────────────────────────────────────
const techCols = [2340, 2340, 2340, 2340];
const techData = [
  ["Runtime & Framework", "Database", "Communication", "DevOps & Cloud"],
  ["Node.js + Express.js", "MongoDB / PostgreSQL", "Firebase FCM (Push)", "AWS / GCP"],
  ["REST API (JSON)", "Redis (Queue/Cache)", "MSG91 / Twilio (SMS)", "Docker + GitHub Actions"],
  ["JWT / OAuth2 Auth", "S3 (File Storage)", "Nodemailer (Email)", "Swagger / OpenAPI"],
  ["PDFKit / Puppeteer", "Bull (Job Queue)", "WebSockets (Real-time)", "Jest (Unit Testing)"],
];

const techTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: techCols,
  rows: techData.map(
    (row, ri) =>
      new TableRow({
        children: row.map(
          (text, ci) =>
            new TableCell({
              borders,
              width: { size: techCols[ci], type: WidthType.DXA },
              shading: { fill: ri === 0 ? HEADER_BG : ri % 2 === 0 ? WHITE : ROW_ALT, type: ShadingType.CLEAR },
              margins: tightMargins,
              children: [
                new Paragraph({
                  alignment: AlignmentType.CENTER,
                  children: [
                    new TextRun({
                      text,
                      bold: ri === 0,
                      size: ri === 0 ? 19 : 18,
                      color: ri === 0 ? WHITE : DARK_TEXT,
                      font: "Arial",
                    }),
                  ],
                }),
              ],
            })
        ),
      })
  ),
});

// ── TERMS TABLE ───────────────────────────────────────────────────────────────
const termsCols = [4600, 4760];
const termsTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: termsCols,
  rows: [
    new TableRow({
      children: [
        new TableCell({
          borders: noBorders,
          shading: { fill: ROW_ALT, type: ShadingType.CLEAR },
          margins: cellMargins,
          width: { size: 4600, type: WidthType.DXA },
          children: [
            new Paragraph({
              spacing: { before: 40, after: 60 },
              children: [new TextRun({ text: "PAYMENT TERMS", bold: true, size: 20, color: BRAND, font: "Arial" })],
            }),
            new Paragraph({
              spacing: { before: 0, after: 30 },
              children: [
                new TextRun({ text: "30% — Advance at project kickoff", size: 19, color: DARK_TEXT, font: "Arial" }),
              ],
            }),
            new Paragraph({
              spacing: { before: 0, after: 30 },
              children: [
                new TextRun({ text: "40% — On completion of core modules", size: 19, color: DARK_TEXT, font: "Arial" }),
              ],
            }),
            new Paragraph({
              spacing: { before: 0, after: 30 },
              children: [
                new TextRun({
                  text: "30% — On final delivery & UAT sign-off",
                  size: 19,
                  color: DARK_TEXT,
                  font: "Arial",
                }),
              ],
            }),
            new Paragraph({
              spacing: { before: 30, after: 60 },
              children: [
                new TextRun({ text: "GST @ 18% applicable on invoices", size: 18, color: "AA3300", font: "Arial" }),
              ],
            }),
          ],
        }),
        new TableCell({
          borders: noBorders,
          shading: { fill: WHITE, type: ShadingType.CLEAR },
          margins: cellMargins,
          width: { size: 4760, type: WidthType.DXA },
          children: [
            new Paragraph({
              spacing: { before: 40, after: 60 },
              children: [
                new TextRun({ text: "TERMS & CONDITIONS", bold: true, size: 20, color: BRAND, font: "Arial" }),
              ],
            }),
            new Paragraph({
              spacing: { before: 0, after: 30 },
              children: [
                new TextRun({
                  text: "Quote valid for 30 days from date of issue",
                  size: 19,
                  color: DARK_TEXT,
                  font: "Arial",
                }),
              ],
            }),
            new Paragraph({
              spacing: { before: 0, after: 30 },
              children: [
                new TextRun({
                  text: "Third-party costs (SMS, cloud hosting) excluded",
                  size: 19,
                  color: DARK_TEXT,
                  font: "Arial",
                }),
              ],
            }),
            new Paragraph({
              spacing: { before: 0, after: 30 },
              children: [
                new TextRun({
                  text: "Scope changes billed at ₹1,000/hr additionally",
                  size: 19,
                  color: DARK_TEXT,
                  font: "Arial",
                }),
              ],
            }),
            new Paragraph({
              spacing: { before: 0, after: 30 },
              children: [
                new TextRun({
                  text: "Source code delivered post final payment",
                  size: 19,
                  color: DARK_TEXT,
                  font: "Arial",
                }),
              ],
            }),
            new Paragraph({
              spacing: { before: 0, after: 60 },
              children: [
                new TextRun({
                  text: "6-month bug-fix warranty post delivery",
                  size: 19,
                  color: DARK_TEXT,
                  font: "Arial",
                }),
              ],
            }),
          ],
        }),
      ],
    }),
  ],
});

// ── SIGNATURE TABLE ───────────────────────────────────────────────────────────
const sigCols = [4600, 4760];
const sigTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: sigCols,
  rows: [
    new TableRow({
      children: [
        new TableCell({
          borders: noBorders,
          shading: { fill: WHITE, type: ShadingType.CLEAR },
          margins: cellMargins,
          width: { size: 4600, type: WidthType.DXA },
          children: [
            new Paragraph({
              spacing: { before: 40, after: 200 },
              children: [
                new TextRun({ text: "For YOUR COMPANY NAME", bold: true, size: 20, color: BRAND, font: "Arial" }),
              ],
            }),
            new Paragraph({
              spacing: { before: 0, after: 0 },
              border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "999999", space: 1 } },
              children: [new TextRun("")],
            }),
            new Paragraph({
              spacing: { before: 60, after: 30 },
              children: [new TextRun({ text: "Authorised Signatory", size: 18, color: MID_TEXT, font: "Arial" })],
            }),
            new Paragraph({
              spacing: { before: 0, after: 30 },
              children: [
                new TextRun({ text: "Name: _____________________________", size: 18, color: MID_TEXT, font: "Arial" }),
              ],
            }),
            new Paragraph({
              spacing: { before: 0, after: 40 },
              children: [
                new TextRun({ text: "Date: ______________________________", size: 18, color: MID_TEXT, font: "Arial" }),
              ],
            }),
          ],
        }),
        new TableCell({
          borders: noBorders,
          shading: { fill: WHITE, type: ShadingType.CLEAR },
          margins: cellMargins,
          width: { size: 4760, type: WidthType.DXA },
          children: [
            new Paragraph({
              spacing: { before: 40, after: 200 },
              children: [
                new TextRun({
                  text: "For BluDoc Healthcare Pvt. Ltd.",
                  bold: true,
                  size: 20,
                  color: BRAND,
                  font: "Arial",
                }),
              ],
            }),
            new Paragraph({
              spacing: { before: 0, after: 0 },
              border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "999999", space: 1 } },
              children: [new TextRun("")],
            }),
            new Paragraph({
              spacing: { before: 60, after: 30 },
              children: [new TextRun({ text: "Authorised Signatory", size: 18, color: MID_TEXT, font: "Arial" })],
            }),
            new Paragraph({
              spacing: { before: 0, after: 30 },
              children: [
                new TextRun({ text: "Name: _____________________________", size: 18, color: MID_TEXT, font: "Arial" }),
              ],
            }),
            new Paragraph({
              spacing: { before: 0, after: 40 },
              children: [
                new TextRun({ text: "Date: ______________________________", size: 18, color: MID_TEXT, font: "Arial" }),
              ],
            }),
          ],
        }),
      ],
    }),
  ],
});

// ── DOCUMENT ─────────────────────────────────────────────────────────────────
const doc = new Document({
  styles: {
    default: {
      document: { run: { font: "Arial", size: 20, color: DARK_TEXT } },
    },
  },
  sections: [
    {
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 720, right: 1080, bottom: 720, left: 1080 },
        },
      },
      footers: {
        default: new Footer({
          children: [
            new Paragraph({
              alignment: AlignmentType.CENTER,
              border: { top: { style: BorderStyle.SINGLE, size: 4, color: BRAND, space: 4 } },
              spacing: { before: 80, after: 0 },
              children: [
                new TextRun({
                  text: "This quotation is system-generated and valid without signature until accepted. ",
                  size: 16,
                  color: "888888",
                  font: "Arial",
                }),
                new TextRun({ text: "Page ", size: 16, color: "888888", font: "Arial" }),
                new TextRun({ children: [PageNumber.CURRENT], size: 16, color: "888888", font: "Arial" }),
              ],
            }),
          ],
        }),
      },
      children: [
        headerTable,
        spacer(200),

        // Client & project info
        clientTable,
        spacer(200),

        // Scope of work
        sectionHeading("Scope of Work & Cost Breakdown"),
        spacer(80),
        scopeTable,
        spacer(80),

        new Paragraph({
          spacing: { before: 0, after: 200 },
          children: [
            new TextRun({
              text: "* Final hours may vary based on detailed requirements. A fixed-price contract can be agreed at ₹4,25,000 (mid-range) upon scope finalization.",
              size: 17,
              color: "AA3300",
              italics: true,
              font: "Arial",
            }),
          ],
        }),

        // Deliverables
        sectionHeading("What's Included"),
        spacer(60),
        ...[
          "Complete Node.js REST API with all 5 feature modules",
          "Swagger / OpenAPI documentation for all endpoints",
          "Unit and integration test coverage (Jest)",
          "Docker containerization and CI/CD pipeline setup",
          "Deployment to staging and production environment (AWS/GCP)",
          "Source code with inline documentation (Git repository)",
          "6-month post-delivery bug fix support",
          "Bi-weekly progress reports and sprint demos",
        ].map(
          item =>
            new Paragraph({
              spacing: { before: 0, after: 60 },
              numbering: { reference: "checkmarks", level: 0 },
              children: [new TextRun({ text: item, size: 20, color: DARK_TEXT, font: "Arial" })],
            })
        ),
        spacer(60),

        // What's NOT included
        sectionHeading("Exclusions (Not in Scope)"),
        spacer(60),
        ...[
          "Mobile app development (Android / iOS) — API only",
          "Third-party service costs: MSG91/Twilio SMS credits, AWS/GCP hosting fees, Play Store fees",
          "Content creation, patient data migration, or integration with legacy systems",
          "DPDP / HIPAA compliance audit (available as add-on at ₹50,000–₹80,000)",
        ].map(
          item =>
            new Paragraph({
              spacing: { before: 0, after: 60 },
              numbering: { reference: "crosses", level: 0 },
              children: [new TextRun({ text: item, size: 20, color: DARK_TEXT, font: "Arial" })],
            })
        ),
        spacer(60),

        // Tech stack
        sectionHeading("Technology Stack"),
        spacer(80),
        techTable,
        spacer(200),

        // Terms
        sectionHeading("Payment Terms & Conditions"),
        spacer(80),
        termsTable,
        spacer(200),

        // Signature
        sectionHeading("Acceptance & Authorization"),
        spacer(80),
        new Paragraph({
          spacing: { before: 0, after: 120 },
          children: [
            new TextRun({
              text: "By signing below, both parties agree to the scope, cost, and terms outlined in this quotation.",
              size: 19,
              color: MID_TEXT,
              font: "Arial",
            }),
          ],
        }),
        sigTable,
      ],
    },
  ],
  numbering: {
    config: [
      {
        reference: "checkmarks",
        levels: [
          {
            level: 0,
            format: LevelFormat.BULLET,
            text: "\u2713",
            alignment: AlignmentType.LEFT,
            style: {
              run: { color: "1A6B35", bold: true, size: 20, font: "Arial" },
              paragraph: { indent: { left: 480, hanging: 320 }, spacing: { after: 40 } },
            },
          },
        ],
      },
      {
        reference: "crosses",
        levels: [
          {
            level: 0,
            format: LevelFormat.BULLET,
            text: "\u2717",
            alignment: AlignmentType.LEFT,
            style: {
              run: { color: "AA3300", bold: true, size: 20, font: "Arial" },
              paragraph: { indent: { left: 480, hanging: 320 }, spacing: { after: 40 } },
            },
          },
        ],
      },
    ],
  },
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("./BluDoc_Quotation_2025.docx", buffer);
  console.log("Done");
});
