import unicodedata

def slugify(var):
    var = var.split("[")[0].strip()
    var = var.split("/")[0].strip()
    var = var.replace("(", "").replace(")", "")
    var = unicodedata.normalize('NFKD', var)
    var = "".join([c for c in var if not unicodedata.combining(c)])
    var = var.replace(" - ", "_")
    var = var.replace(":", "").replace('?', "")
    var = var.replace('’', '').replace("'", "")
    var = var.replace(',', "").replace(".", "")
    var = var.replace(" ", "_")
    return var