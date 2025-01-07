import sys
import os
import json
from slugify import slugify
from jinja2 import Template


print("Usage: python ./TEMPLATE/generator.py 'year' 'ctf title'")

year, title = sys.argv[1:]
title_file = title.replace(" ", "_")

with open(f"./{year}/{title_file}/info.json") as info_file:
    info = dict(json.loads(info_file.read())).items()
    probs = {type: [(prob, slugify(prob)) for prob in probs]
             for type, probs in info}.items()

with open("./TEMPLATE/[CTF-TITLE]/README.md") as ctf_tmpl_file:
    ctf_tmpl = Template(ctf_tmpl_file.read())
    ctf = ctf_tmpl.render(title=title, probs=probs)
    with open(f"./{year}/{title_file}/README.md", "w") as ctf_file:
        ctf_file.write(ctf)

with open("./TEMPLATE/[CTF-TITLE]/[PROBLEM-TITLE]/README.md") as prob_tmpl_file:
    prob_tmpl = Template(prob_tmpl_file.read())
    for _, probs in probs:
        for k, v in probs:
            os.makedirs(f"./{year}/{title_file}/{v}", exist_ok=True)
            prob = prob_tmpl.render(title=k)
            with open(f"./{year}/{title_file}/{v}/README.md", "w") as prob_file:
                prob_file.write(prob)

print("done.")
