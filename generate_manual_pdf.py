from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import ListFlowable, ListItem, Paragraph, Preformatted, SimpleDocTemplate, Spacer


OUTPUT_FILE = "Guia-edicion-ScanMatic.pdf"


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="BodySmall",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10.5,
            leading=14,
            spaceAfter=8,
            alignment=TA_LEFT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SectionTitle",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=18,
            textColor=colors.HexColor("#0b2948"),
            spaceBefore=8,
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Note",
            parent=styles["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor("#444444"),
            backColor=colors.HexColor("#f1f5f9"),
            borderPadding=8,
            borderColor=colors.HexColor("#d7e0ea"),
            borderWidth=0.5,
            borderRadius=4,
            spaceBefore=6,
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CodeBlock",
            fontName="Courier",
            fontSize=8.8,
            leading=11,
            backColor=colors.HexColor("#f8fafc"),
            borderPadding=8,
            borderColor=colors.HexColor("#d7e0ea"),
            borderWidth=0.5,
            leftIndent=0,
            rightIndent=0,
            spaceBefore=4,
            spaceAfter=10,
        )
    )
    return styles


def bullet_list(items, style):
    return ListFlowable(
        [
            ListItem(Paragraph(item, style), leftIndent=10)
            for item in items
        ],
        bulletType="bullet",
        start="circle",
        leftIndent=14,
        bulletFontName="Helvetica",
        bulletFontSize=8,
    )


def section(title, paragraphs, bullets=None, code=None, note=None, styles=None):
    story = [Paragraph(title, styles["SectionTitle"])]
    for paragraph in paragraphs:
        story.append(Paragraph(paragraph, styles["BodySmall"]))
    if bullets:
        story.append(bullet_list(bullets, styles["BodySmall"]))
        story.append(Spacer(1, 0.16 * cm))
    if code:
        story.append(Preformatted(code, styles["CodeBlock"]))
    if note:
        story.append(Paragraph(note, styles["Note"]))
    return story


def build_pdf():
    styles = build_styles()
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=A4,
        rightMargin=1.7 * cm,
        leftMargin=1.7 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
        title="Guia de edicion manual de ScanMatic",
        author="Codex",
    )

    story = []

    story.append(Paragraph("Guia practica para editar tu pagina web ScanMatic", styles["Title"]))
    story.append(Spacer(1, 0.2 * cm))
    story.append(
        Paragraph(
            "Esta guia esta hecha para tu archivo actual <b>index.html</b>. Explica que bloque controla cada zona de la pagina, "
            "como editar textos, estilos y enlaces, y que partes no debes romper si quieres conservar el contador de visitas y clicks.",
            styles["BodySmall"],
        )
    )
    story.append(
        Paragraph(
            "Archivo principal: <b>D:\\ScanMatic-AutoTech\\index.html</b>",
            styles["BodySmall"],
        )
    )
    story.append(
        Paragraph(
            "PDF generado automaticamente para que puedas regenerarlo cuando cambie la pagina.",
            styles["Note"],
        )
    )

    story.extend(
        section(
            "1. Como esta organizada la pagina",
            [
                "Toda la web vive en un solo archivo. El CSS empieza en la linea 7, el contenido HTML visible empieza cerca de la linea 589 y la logica JavaScript empieza en la linea 770.",
                "Eso significa que puedes editar la pagina entera sin tocar otros archivos, salvo que quieras cambiar el logo o el video, que viven como archivos separados en el proyecto.",
            ],
            bullets=[
                "CSS: index.html:7",
                "Video de fondo: index.html:589",
                "Logo: index.html:603",
                "Tarjetas de cursos: index.html:679",
                "Bloque de contacto: index.html:748",
                "Script de contadores: index.html:770",
            ],
            styles=styles,
        )
    )

    story.extend(
        section(
            "2. Cambiar apariencia general",
            [
                "Los colores y medidas base estan en :root. Si quieres cambiar la identidad visual completa, ese es el mejor lugar para empezar.",
                "Las variables controlan colores de fondo, acento, texto, paneles y sombras. Cambiar variables es mas seguro que editar cada regla una por una.",
            ],
            bullets=[
                "Variables globales: index.html:9",
                "Ancho maximo general: --max-width en index.html:24",
                "Color de acento: --accent y --accent-strong",
                "Color de botones: --action",
            ],
            code=""":root {
    --bg: #07111f;
    --accent: #ff5c5c;
    --action: #0d7ce8;
    --max-width: 1240px;
}""",
            note="Si cambias nombres de variables, luego debes actualizar todas las reglas que las usan.",
            styles=styles,
        )
    )

    story.extend(
        section(
            "3. Hacer mas visible o menos visible el video",
            [
                "El video real se dibuja en .video-background y la capa que lo oscurece esta en .overlay. La transparencia que ves delante depende sobre todo de esos dos bloques.",
                "Si quieres ver mas el video, baja los valores RGBA de .overlay y de los paneles translucidoss como .hero-copy, .hero-aside, .courses y .contact-section.",
            ],
            bullets=[
                "Video y ajuste del objeto: index.html:54",
                "Capa oscura principal: index.html:73",
                "Panel principal hero: index.html:110",
                "Panel cursos: index.html:385 y 466",
            ],
            code=""".overlay {
    background:
        linear-gradient(180deg,
        rgba(4, 8, 16, 0.22) 0%,
        rgba(4, 8, 16, 0.52) 48%,
        rgba(3, 7, 13, 0.72) 100%);
}

.hero-copy,
.hero-aside {
    background: linear-gradient(180deg,
        rgba(11, 25, 44, 0.52),
        rgba(8, 18, 33, 0.65));
}""",
            note="Mas bajo el alfa = mas visible el video. Si bajas demasiado, el texto pierde contraste.",
            styles=styles,
        )
    )

    story.extend(
        section(
            "4. Editar textos del encabezado",
            [
                "El hero principal es la primera pantalla de la web. Ahi cambias el nombre visible, la frase principal, el subtitulo y los botones.",
                "Esta zona es la que mas impacta conversion y claridad. Cambia textos con cuidado para no romper las etiquetas ni clases.",
            ],
            bullets=[
                "Titulo principal: cerca de index.html:608",
                "Parrafo principal: cerca de index.html:609",
                "Boton Explorar modulos: cerca de index.html:615",
                "Boton Hablar con soporte: cerca de index.html:616",
            ],
            code="""<h1>ScanMatic <span>Autotech</span></h1>
<p class="hero-lead">
    Tu texto comercial aqui.
</p>
<a href="#modulos" class="btn btn-primary">Explorar modulos</a>""",
            styles=styles,
        )
    )

    story.extend(
        section(
            "5. Editar logo y video",
            [
                "El logo y el video no estan dentro del HTML como contenido incrustado; solo se llaman por nombre de archivo.",
                "Si reemplazas el archivo manteniendo el mismo nombre, no hace falta tocar el HTML. Si cambias el nombre, si debes editar el src.",
            ],
            bullets=[
                "Video: oscilograma.mp4 llamado en index.html:591",
                "Logo: logo.png llamado en index.html:603",
            ],
            code="""<source src="oscilograma.mp4" type="video/mp4">
<img src="logo.png" alt="Logo de ScanMatic Autotech">""",
            note="Mantener el mismo nombre de archivo es la forma mas segura de actualizar recursos visuales.",
            styles=styles,
        )
    )

    story.extend(
        section(
            "6. Editar modulos y enlaces de cursos",
            [
                "Cada modulo es una tarjeta article con clase course-card. Dentro de cada tarjeta puedes cambiar numero, titulo, descripcion, enlace y clave del contador.",
                "Si solo cambias el titulo o el enlace, el contador puede seguir igual. Si duplicas o creas un modulo nuevo, debes crear tambien una nueva clave unica data-course-key y data-click-display.",
            ],
            bullets=[
                "Primer modulo: index.html:679",
                "Cada enlace de curso usa class=course-link",
                "Cada modulo tiene una clave como modulo-01",
            ],
            code="""<article class="course-card">
    <span class="module-tag">Modulo 01</span>
    <h3>Titulo del curso</h3>
    <p>Descripcion del curso</p>
    <span class="click-count" data-click-display="modulo-01">Clicks: <strong>...</strong></span>
    <a href="https://tu-enlace" class="course-link" data-course-key="modulo-01">Ver informacion</a>
</article>""",
            note="Las dos claves deben coincidir: data-click-display='modulo-01' y data-course-key='modulo-01'.",
            styles=styles,
        )
    )

    story.extend(
        section(
            "7. Editar contacto y botones externos",
            [
                "El bloque de contacto esta casi al final del HTML y es facil de editar. Aqui puedes cambiar telefono de WhatsApp, usuario de Telegram y textos de ayuda.",
                "No cambies solo el texto visible; si el enlace cambia, actualiza tambien el href.",
            ],
            bullets=[
                "Seccion contacto: index.html:748",
                "WhatsApp y Telegram visibles en el mismo bloque",
            ],
            code="""<a href="https://wa.me/51944085764" class="contact-link whatsapp">WhatsApp soporte</a>
<a href="https://t.me/ScanMatic_AutoTech" class="contact-link telegram">Comunidad Telegram</a>""",
            styles=styles,
        )
    )

    story.extend(
        section(
            "8. Como funcionan los contadores",
            [
                "Los contadores no se guardan dentro del HTML ni en GitHub. Se guardan en un servicio externo llamado CountAPI, usando la URL base configurada en el script.",
                "La visita total se incrementa al cargar la pagina. Los clicks se incrementan cuando el usuario pulsa el boton de un modulo.",
            ],
            bullets=[
                "Inicio del script: index.html:770",
                "API del contador: index.html:772",
                "Lectura de botones de cursos: index.html:774",
                "Incremento de visitas: index.html:793",
                "Lectura de valor actual: index.html:806",
                "Evento click por modulo: index.html:865",
            ],
            code="""const COUNTER_API = "https://countapi.mileshilliard.com/api/v1";
const courseLinks = Array.from(document.querySelectorAll("[data-course-key]"));

fetch(COUNTER_API + "/hit/" + makeCounterKey("click-" + key), {
    method: "GET",
    cache: "no-store",
    keepalive: true
});""",
            note="Si borras data-course-key o data-click-display, el contador de ese modulo deja de funcionar.",
            styles=styles,
        )
    )

    story.extend(
        section(
            "9. Cambios comunes que puedes hacer tu mismo",
            [
                "Estas son las ediciones manuales mas seguras si todavia estas aprendiendo.",
            ],
            bullets=[
                "Cambiar textos visibles sin tocar clases ni atributos.",
                "Cambiar enlaces href manteniendo las comillas y el formato.",
                "Cambiar colores editando solo :root.",
                "Cambiar transparencia tocando solo rgba(...) en .overlay y paneles.",
                "Cambiar el video o logo manteniendo el mismo nombre de archivo.",
                "Duplicar un modulo copiando una tarjeta entera y usando una nueva clave unica.",
            ],
            styles=styles,
        )
    )

    story.extend(
        section(
            "10. Errores que debes evitar",
            [
                "La mayoria de los errores en paginas de un solo archivo vienen por borrar comillas, signos mayor-que, cerrar mal una etiqueta o cambiar un atributo que el script necesita.",
            ],
            bullets=[
                "No borres class='course-link' en los botones de cursos.",
                "No borres data-course-key ni data-click-display si quieres contadores.",
                "No cambies la URL COUNTER_API salvo que sepas que el servicio responde.",
                "No mezcles nombres de modulo. Si el boton usa modulo-03, el display tambien debe usar modulo-03.",
                "No metas texto dentro del bloque script si no es codigo JavaScript valido.",
            ],
            styles=styles,
        )
    )

    story.extend(
        section(
            "11. Flujo recomendado para editar sin romper",
            [
                "Si vas a tocar la pagina a mano, sigue este orden corto. Es el que menos errores produce.",
            ],
            bullets=[
                "1. Edita textos y enlaces.",
                "2. Guarda el archivo.",
                "3. Abre index.html en el navegador.",
                "4. Revisa video, botones y contadores.",
                "5. Si algo falla, vuelve al ultimo cambio pequeño y corrige.",
                "6. Cuando todo se vea bien, sube el cambio a GitHub.",
            ],
            styles=styles,
        )
    )

    story.extend(
        section(
            "12. Archivos de tu proyecto",
            [
                "Tu proyecto actual es muy simple. Eso facilita editarlo, pero tambien significa que un error en index.html afecta toda la pagina.",
            ],
            bullets=[
                "index.html: estructura, estilo y logica",
                "logo.png: logotipo",
                "oscilograma.mp4: video de fondo",
                "Guia-edicion-ScanMatic.pdf: este manual",
                "generate_manual_pdf.py: script para regenerar este manual",
            ],
            note="Si mas adelante separas CSS y JavaScript en archivos distintos, la web sera mas facil de mantener.",
            styles=styles,
        )
    )

    doc.build(story)


if __name__ == "__main__":
    build_pdf()
