import pdb
import hashlib


def get_sha1_checksum(file):
    '''
    returns sha1 checksum
    '''
    BUF_SIZE = 65536
    sha1 = hashlib.sha1()

    with open(file, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)
    return sha1
    

def set_modified_element(rt, params):
    '''
    sets to 'val' the attribute of element in root 'rt' with position 'pos'
    '''
    val, pos = params
    if len(pos) == 1:
        rt[pos[0]].text = str(val)
    elif len(pos) == 2:
        rt[pos[0]][pos[1]].text = str(val)
    elif len(pos) == 3:
        rt[pos[0]][pos[1]][pos[2]].text = str(val)
    elif len(pos) == 4:
        rt[pos[0]][pos[1]][pos[2]][pos[3]].text = str(val)
    elif len(pos) == 5:
        rt[pos[0]][pos[1]][pos[2]][pos[3]][pos[4]].text = str(val)
    elif len(pos) == 6:
        rt[pos[0]][pos[1]][pos[2]][pos[3]][pos[4]][pos[5]].text = str(val)
    elif len(pos) == 7:
        rt[pos[0]][pos[1]][pos[2]][pos[3]][pos[4]][pos[5]][pos[6]].text = str(val)
    elif len(pos) == 8:
        rt[pos[0]][pos[1]][pos[2]][pos[3]][pos[4]][pos[5]][pos[6]][pos[7]].text = str(val)


def set_modified_val(rt, params):
    '''
    sets to 'val' the value of item with key 'ky' for the element in root 'rt' with position 'pos'
    '''
    val, ky, pos = params
    if len(pos) == 1:
        rt[pos[0]].attrib[ky] = val
    elif len(pos) == 2:
        rt[pos[0]][pos[1]].attrib[ky] = val
    elif len(pos) == 3:
        rt[pos[0]][pos[1]][pos[2]].attrib[ky] = val
    elif len(pos) == 4:
        rt[pos[0]][pos[1]][pos[2]][pos[3]].attrib[ky] = val
    elif len(pos) == 5:
        rt[pos[0]][pos[1]][pos[2]][pos[3]][pos[4]].attrib[ky] = val
    elif len(pos) == 6:
        rt[pos[0]][pos[1]][pos[2]][pos[3]][pos[4]][pos[5]].attrib[ky] = val
    elif len(pos) == 7:
        rt[pos[0]][pos[1]][pos[2]][pos[3]][pos[4]][pos[5]][pos[6]].attrib[ky] = val
    elif len(pos) == 8:
        rt[pos[0]][pos[1]][pos[2]][pos[3]][pos[4]][pos[5]][pos[6]][pos[7]].attrib[ky] = val


def get_prefix(last_name, first_name):
    '''
    5 or more lowercase letters which will be used to create the client's username.
    IB will add 3 or 4 numbers to the prefix to create the username.

    Below function attempts to construct 5 letter lower case prefix from last_name and
    first_name. If not enough letters are available, dummy_prefix is used. If the resulting
    prefix contains any non alphabetic these are replaced by 'b'. 
    '''
    dummy_prefix = 'abcde'
    prefix = ''
    if len(last_name) >= 5:
        prefix = last_name[:5]
    elif len(last_name) == 4 and len(first_name) >= 1:
        prefix = last_name + first_name[:1]
    elif len(last_name) == 3 and len(first_name) >= 2:
        prefix = last_name + first_name[:2]
    elif len(last_name) == 2 and len(first_name) >= 3:
        prefix = last_name + first_name[:3]
    elif len(last_name) == 1 and len(first_name) >= 4:
        prefix = last_name + first_name[:4]
    elif len(last_name) == 0 and len(first_name) >= 5:
        prefix = last_name + first_name[:5]
    else:
        prefix = dummy_prefix

    prefix = ''.join([c if c.isalpha() else 'x' for c in prefix])

    return prefix.lower()

     
def show_tree(root):
    '''
    shows up to the top 8 elements in root
    '''
    for i in range(len(root)):
        print(i, root[i].tag, root[i].text, root[i].attrib)
        for j in range(len(root[i])):
            print(i, j, root[i][j].tag, root[i][j].text, root[i][j].attrib)
            for k in range(len(root[i][j])):
                print(i, j, k, root[i][j][k].tag, root[i][j][k].text, root[i][j][k].attrib)
                for m in range(len(root[i][j][k])):
                    print(i, j, k, m, root[i][j][k][m].tag, root[i][j][k][m].text, root[i][j][k][m].attrib)
                    for n in range(len(root[i][j][k][m])):
                        print(i, j, k, m, n, root[i][j][k][m][n].tag, root[i][j][k][m][n].text, root[i][j][k][m][n].attrib)
                        for p in range(len(root[i][j][k][m][n])):
                            print(i, j, k, m, n, p, root[i][j][k][m][n][p].tag, root[i][j][k][m][n][p].text, root[i][j][k][m][n][p].attrib)
                            for q in range(len(root[i][j][k][m][n][p])):
                                print(i, j, k, m, n, p, q, root[i][j][k][m][n][p][q].tag, root[i][j][k][m][n][p][q].text, root[i][j][k][m][n][p][q].attrib)
                                for r in range(len(root[i][j][k][m][n][p][q])):
                                    print(i, j, k, m, n, p, q, r, root[i][j][k][m][n][p][q][r].tag, root[i][j][k][m][n][p][q][r].text, root[i][j][k][m][n][p][q][r].attrib)
                                    print('--- NB there may be more levels with child elements, but these will not be shown ---')
