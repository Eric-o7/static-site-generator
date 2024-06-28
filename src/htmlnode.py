class HTMLNode():
    def __init__(self, value=None, children=None, props=None, tag=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        result = ""
        for x,y in self.props.items():
            result +=  f' {x}="{y}"'
        return result
    
    def __repr__(self):
        return f"TAG = {self.tag}, VALUE = {self.value}, CHILDREN = {self.children}, PROPS = {self.props}"
    
class LeafNode(HTMLNode):
    def __init__(self, value, props, tag=None):
        super().__init__()
        self.value = value
        self.props = props
        self.tag = tag

    def to_html(self):
        if self.tag is None:
            raise ValueError
        if len(self.tag) <= 2:
            listed = []
            for t in self.tag:
                if len(t) == 1:
                    listed.append(f"<{t}>")
                else:
                    listed.append(t)
            listed.append(f"</{self.tag[0]}>")
            return "".join(listed)
        else:
            url_list = []
            for i in self.tag: 
                if type(i) == dict:
                    s1 = str(i)
                    s1 = s1.replace(" ","")
                    #create a dictionary to iterate into a replace function
                    #not especially space saving right now but I want to keep it for reference
                    chars_to_replace = {"}":">", "{": f"<{self.tag[0]} ", "'":'"'}
                    for key, value in chars_to_replace.items():
                        s1 = s1.replace(key, value)
                    s1 = s1.replace(":","=",1)
                    s1 = s1.replace('"',"",2)
                    url_list.append(s1)
            url_list.append(self.tag[1])
            url_list.append(f"</{self.tag[0]}>")
            return "".join(url_list)
        
    