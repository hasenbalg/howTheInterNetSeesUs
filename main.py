import urllib
import urllib2
import re

# body_parts = ("kopf", "hals", "schulter", "oberarm", "unterarm", "hand", "brust", "bauch", "ruecken", "huefte", "oberschenkel", "unterschenkel", "fuss")
# len(body_parts)

# matrix = [len(body_parts)][len(body_parts)]


def extract_body_parts_from_3d_file(path):
    import json
    body_parts = []
    with open(path) as data_file:
        data = json.load(data_file)
    data = data["bones"]
    for bone in data:
        if bone["name"] != "root":
            name = bone["name"].replace("_l", "").replace("_r", "").replace("_", "+")
            body_parts.append(name)
    body_parts = list(set(body_parts)) #remove duplicats
    return body_parts;

body_parts = extract_body_parts_from_3d_file("res/human2.json")
matrix = [[0 for x in range(len(body_parts))] for y in range(len(body_parts))]

def write_to_file(text):
    target = open("result.csv", 'w')
    target.write(text);
    target.close()

def extract_number(text):
    # 'id="resultStats".*?>.+?([\d\.]+?)\s.+?<'
     p = re.compile('id="resultStats".*?>.+?([\d\.]+?)\s.+?<')
     return p.search(text).group(1).replace(".","")   # returns first match of of eg 160.000.000 and remove dots

def make_csv():
    output = "," # first field is blank
    x = 0
    # table head
    for body_part in body_parts:
        output += body_part.replace("+","_") + ","
    # ditch last comma and add a line break
    output = output.rstrip(',') + "\n"
    for row in matrix:
        # first column
        output += body_parts[x].replace("+","_") + ","
        x += 1
        for value in row:
            output += str(value) + ","
        # ditch last comma and add a line break
        output = output.rstrip(',') + "\n"
    # remove last comma
    return output.rstrip(',') # http://stackoverflow.com/a/12625648

def main():
    print matrix
    x,y = 0,0
    for first_word in body_parts:
        for second_word in body_parts:
            if second_word != first_word:
                # http://stackoverflow.com/a/12797391
                url = "http://www.google.com/search?q=" + first_word + "+" + second_word;
                opener = urllib2.build_opener()
                opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                result = opener.open(url).read()
                result = extract_number(result)
            else:
                result = 0;
            matrix[x][y] = result
            print body_parts[x] + " - " + body_parts[y]  + " - " + str(result)
            y += 1
        x += 1
        y = 0
    write_to_file(make_csv())


if __name__ == '__main__':
    main()
