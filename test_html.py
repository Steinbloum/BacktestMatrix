from constructors import RandomWord
r = RandomWord()

def gen_words(amount):
    ls = []
    for i in range(amount):
        ls.append(r.word())
    string = ' '.join(ls)
    return string
print(gen_words(5))

with open('ui/displaytxt.html', 'w') as f:
    f.write('''<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Matrix Configuration</title>
        </head>
        <body>
            <div class="display-text">
                <p>{}</p>
            </div>
        </body>
        </html>'''.format(gen_words(5)))
f.close


