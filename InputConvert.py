def ColConvert(col):
    if len(col)==1:
        return ord(col)-ord('A')+1

    elif len(col)>1:
        col = col[::-1]
        sum = 0
        for i in range(len(col)):
            sum += (ord(col[i])-ord('A')+1)*(26**i)

        return sum

def GroupConvert(groups, metadata):
    groups = groups.split(',')
    groups = [i.strip(' ') for i in groups]
    metadata = [i.strip(' ') for i in metadata]
    rows=[]
    for i in range(len(metadata)):
        if metadata[i] in groups:
           rows.append(i+1)

    return rows

def ColorConvert(color):
    color = color.split(',')
    color = [i.strip(' ') for i in color]
    return color