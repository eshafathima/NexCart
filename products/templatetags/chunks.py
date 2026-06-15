from django import template

register=template.Library()

@register.filter(name='chunks')
def chunks(list_data,chunk_size):
    chunk=[]
    i=0
    chunk_size=int(chunk_size)
    if not list_data:
        return[]
    for x in list_data:
        chunk.append(x)
        i+=1
        if i==chunk_size:
            yield chunk
            chunk=[]
            i=0
    yield chunk


