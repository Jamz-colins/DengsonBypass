"""
Database 120+ domain URL shortener standar & redirect wrapper
untuk DengsonBypass.
"""

KNOWN_SHORTENERS: set[str] = {
    # General & Popular URL Shorteners
    "bit.ly", "bitly.com", "j.mp", "tinyurl.com", "t.co", "is.gd", "v.gd",
    "ow.ly", "buff.ly", "cutt.ly", "rebrand.ly", "rb.gy", "shorturl.at",
    "s.id", "tiny.cc", "bl.ink", "snip.ly", "soo.gd", "s2r.co", "clck.ru",
    "vk.cc", "u.to", "x.co", "t.ly", "short.io", "short.cm", "kutt.it",
    "gg.gg", "qps.ru", "cli.gs", "ity.im", "tr.im", "bit.do", "mcaf.ee",
    "su.pr", "twurl.nl", "ur1.ca", "doiop.com", "url.ie", "chilp.it",
    "dft.ba", "filoops.info", "hive.am", "idek.net", "korta.nu", "liltext.com",
    "lin.cr", "linkbee.com", "lnkd.in", "db.tt", "qr.ae", "qr.net", "po.st",
    "shar.es", "sp2.ro", "t2m.io", "tinyarrows.com", "tinylink.in",
    "tinyplaza.com", "tny.im", "to.ly", "togoto.us", "tr5.in", "tra.kz",
    "tweez.me", "u.nu", "ub0.cc", "ulimit.com", "url4.eu", "urlao.com",
    "urlbrief.com", "urlcover.com", "urlcut.com", "urlenco.de", "urlhawk.com",
    "urlin.it", "urlkiss.com", "urlpass.com", "urls.im", "urlx.ie", "urlz.fr",
    "vurl.com", "w3t.org", "waa.ai", "xurl.es", "xurl.jp", "yep.it",
    "yfrog.com", "zpag.es", "zi.ma",
    # Official Tech, Media & Brand Short Domains
    "goo.gl", "g.co", "youtu.be", "fb.me", "fb.watch", "instagr.am",
    "amzn.to", "amzn.eu", "a.co", "aka.ms", "msft.it", "apple.co",
    "git.io", "redd.it", "pin.it", "spoti.fi", "snd.sc", "wp.me",
    "nyti.ms", "wapo.st", "bbc.in", "cnn.it", "for.tn", "ti.me",
    "disq.us", "flic.kr", "gph.is", "imgur.com", "sched.co", "zoom.us",
}

# Domain pembungkus redirect beserta nama parameter query tujuan aslinya
REDIRECT_WRAPPERS: dict[str, list[str]] = {
    "google.com": ["q", "url"],
    "l.facebook.com": ["u"],
    "lm.facebook.com": ["u"],
    "m.facebook.com": ["u"],
    "l.instagram.com": ["u"],
    "youtube.com": ["q"],
    "l.messenger.com": ["u"],
    "vk.com": ["to"],
    "outgoing.prod.mozaws.net": ["url"],
    "statics.teams.cdn.office.net": ["url"],
    "safelinks.protection.outlook.com": ["url"],
    "urldefense.proofpoint.com": ["u"],
    "gate.sc": ["url"],
    "steamcommunity.com": ["url"],
}

# Parameter query umum jika path mengandung pola redirect
GENERIC_REDIRECT_PARAMS: tuple[str, ...] = (
    "url", "u", "q", "target", "dest", "destination",
    "redir", "redirect", "redirect_uri", "to", "goto", "link",
)

REDIRECT_PATH_HINTS: tuple[str, ...] = (
    "/redirect", "/url", "/away", "/out", "/l.php", "/leave", "/exit", "/linkfilter",
)
