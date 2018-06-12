from django.db import models
import numpy as np
import re

### utilities ###

class IconObj(object):
    """Informations to draw an icon linking to another subject
    (on a causality diagram)"""
    def __init__(self,title,text,pic,color,pos,size,target_id,node_id=None):
        self.title = title
        self.text = text
        self.picture = pic
        self.color = color
        self.pos = pos
        self.size = size
        self.target_id = target_id
        self.node_id = node_id
        
    def norm(self,offset,factor):
        self.pos = [factor*(self.pos[i]+offset[i]) for i in range(2)]
        self.pos = [int(i) for i in self.pos]
        self.size = int(factor*self.size)
        
class ArrowObj(object):
    """To draw arrows on a causality diagram"""
    def __init__(self,pos,color):
        self.pos = pos
        self.color = color
        
    def norm(self,offset,factor):
        pos=[factor*(offset[i[0]%2]+i[1]) for i in enumerate(self.pos)]
        self.pos = [int(i) for i in pos]
                        
class DiagramObj(object):
    """All information needed to draw a causality diagram"""
    def __init__(self,name,icons,pairs,margin,width,height,line_width,
        text_size_factor=3/2):
    
        text_size=text_size_factor*max([i.size for i in icons])
    
        offsetX = - min([i.pos[0]-text_size for i in icons])
        offsetY = - min([i.pos[1]-text_size for i in icons])
        offset = (offsetX,offsetY)
        
        current_width = max([i.pos[0]+text_size for i in icons]) + offset[0]
        current_height = max([i.pos[1]+text_size for i in icons]) + offset[1]
        
        factor = min((width-2*margin)/current_width,
                    (height-2*margin)/current_height)
        offset=[i+margin/factor for i in offset]
        
        vects= [np.array([p[1].pos[0]-p[0].pos[0],p[1].pos[1]-p[0].pos[1]]) 
                for p in pairs]
        lengths = [np.sqrt(np.dot(v,v)) for v in vects]
        start_end = [(p[0].size/le,(le-p[1].size)/le) for p,le in zip(pairs,lengths)]
        pos = [[p[0].pos[i%2]+se[i//2]*v[i%2] for i in range(4)] for p,se,v in zip(pairs,start_end,vects)]
        colors = [p[0].color for p in pairs]
        
        arrows = [ArrowObj(*i) for i in zip(pos,colors)]
        
        [i.norm(offset,factor) for i in icons]
        [i.norm(offset,factor) for i in arrows]
    
        self.name=name
        self.width = int(width)
        self.height = int(height)
        self.line_width = int(line_width)
        self.icons = icons
        self.arrows = arrows
        self.lines = [i for i in arrows]
        self.text_size = int(factor*text_size)
        
        self.offset=offset
        self.factor=factor
        
    def add_arrows(self,arrows,lines):
        arrows=[ArrowObj(*i) for i in arrows]
        lines = [ArrowObj(*i) for i in lines]
        [i.norm(self.offset,self.factor) for i in arrows]
        [i.norm(self.offset,self.factor) for i in lines]
        self.arrows.extend(arrows)
        self.lines.extend(lines)
            
class Dummy(object):
    def __init__(self,dict):
        self.__dict__.update(dict)

def find_links(s):
    offset=0
    a=re.findall("http[^ ]*",s)
    b=re.split("http[^ ]*",s)
    c=[]
    for i,j in zip(a,b[:-1]):
        if re.search("""<a.*href""",j) is None:
            c.append("<a href='%s'>%s</a>"%(i,i))
        else:
            c.append(i)
    res=b[0]
    for i,j in zip(c,b[1:]):
        res+=i+j
    return res
        
POSITIONS = (
    ("L","Left"),
    ("R","Right"),
    ("BR","Bottom Right"),
    ("BL","Bottom Left"),
    ("BC","Bottom Center")
)
        
#################


### Picture storage ###

class PictureDim(models.Model):
    '''Specifies dimensions of an image'''
    # height and width
    height= models.IntegerField(default=0, blank=True)
    width= models.IntegerField(default=0, blank=True)
    
    # rectangle to crop an image
    left= models.IntegerField(default=0, blank=True)
    right= models.IntegerField(default=0, blank=True)
    top= models.IntegerField(default=0, blank=True)
    bottom= models.IntegerField(default=0, blank=True)

    
class Picture(models.Model):
    title = models.CharField(max_length=400, blank=True)
    source = models.CharField(max_length=300, blank=True)
    picture = models.ImageField(upload_to = "ecosyn/pictures/",
                                null = True, blank=True)
    link = models.CharField(max_length=400, blank=True)
    dims = models.ForeignKey(PictureDim, on_delete= models.SET_NULL, 
                                null=True, blank=True)
    def __str__(self):
        return self.title
        
    def resize(self,width=None,height=None):
        pic=self.picture
        size_pic=np.array([pic.width,pic.height])
        d=self.dims
        if d is not None:
            width = width if width is not None else d.width
            height = height if height is not None else d.height
            if width==0:
                width=pic.width
            if height==0:
                height=pic.height
            size_crop=size_pic-np.array([d.left+d.right, d.top+d.bottom])
            if min(size_crop)<=0:
                size_crop=size_pic
            margins=[d.top,0,0,d.left]
        else:
            width = width if width is not None else size_pic[0]
            height = height if height is not None else size_pic[1]
            size_crop=size_pic
            margins=[0]*4

        factor = min(np.array([width,height])/size_crop)
        size_pic=[int(i*factor) for i in size_pic]
        size_crop=[int(i*factor) for i in size_crop]
        margins=[int(-i*factor) for i in margins]
        margins="%dpx %dpx %dpx %dpx"%tuple(margins)
        print(size_pic,size_crop,margins)
        return (size_pic,size_crop,margins)
    
    
class Icon(models.Model):
    title = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=200, blank=True)
    picture = models.ImageField(upload_to = "ecosyn/icons/",
                                null = True, blank=True)
    def __str__(self):
        return self.title


### Main classes ###
        
        
class SujetOrSecteur(models.Model):
    """ Abstract Class for storing topics or reports (ex: "Le charbon")
    
    The main content is stored in <SujetSection> objects
    
    Attributes:
        header_picture : will be placed above the title
        left_picture : optionnally to be placed on the left_picture
        caused_by : <Sujet> topics causing the present issue
        consequence : <Sujet> topics caused by the present issue
    """
    
    name = models.CharField(max_length = 100)
    title = models.CharField(max_length=200)
    short_description = models.CharField(max_length=400, blank=True)
    date_created = models.DateField(auto_now_add = True)
    
    header_picture = models.ForeignKey(Picture, null = True, blank = True,
        on_delete = models.SET_NULL,
        related_name="+")
        
    icon_picture = models.ForeignKey(Icon, null = True, blank = True,
        on_delete = models.SET_NULL,
        related_name="+")
    
    def __str__(self):
        return self.name

    def get_sections(self):
        sec=self.section_set.order_by("order").all()
        res=[]
        order=0
        temp=[]
        for i in sec:
            if i.order!=order:
                res.append(temp)
                temp=[i]
                order=i.order
            else:
                temp.append(i)
        res.append(temp)
        return res
        
    class Meta:
        abstract = True
  
  
class Secteur(SujetOrSecteur):
    """ Subclass of <SujetOrSecteur> for storing reports (ex: "Le charbon")
    
    The main content is stored in <SecteurSection> objects
    
    Attributes:
        name : used internally
        title : Title displayed on the site
        short_description : displayed under the title
        header_picture : will be placed above the title
        left_picture : optionnally to be placed on the left_picture
    """
    color = models.CharField(max_length = 50, default="grey")
    order = models.IntegerField(default = 0)    
 
 
class Sujet(SujetOrSecteur):
    """ Class for storing topics (ex: "Le charbon")
    
    The main content is stored in <SujetSection> objects
    
    Attributes:
        header_picture : will be placed above the title
        left_picture : optionnally to be placed on the left_picture
        causes : <Lien> topics causing the present issue
        consequences : <Lien> topics caused by the present issue
    """
    
    secteur = models.ForeignKey(Secteur, null = True, blank=True,
                               on_delete = models.SET_NULL)

                               
    def __str__(self):
        return self.name
        
    def get_cause_diagram(self, width=500, height = 500):
        """ Prepare the diagram of issues that cause the present ones
        
        pics : <list of Picture> icon of the causes
        colors : <list of str> the corresponding Sector color
        text : <list of str> a short description of the cause
        pos : <list of (x,y) tuples> position of the cause image
        sizes : <list of float> size of the cause image
        
        """
        size_center= 7
        default_size = 3
        distance = 15
        line_width = 2
        margin = 5
        side_angle = 0.7
        
        causes = self.causes.all()
        lien_causes = [lien.cause for lien in causes]
        
        if len(causes)>0:
            # computing position and size of the graphic elements
            sizes= [lien.relative_share for lien in causes]
            sizes= [np.sqrt(i) if i is not None else default_size for i in sizes]
            sizes= [min(i,distance-size_center-2) for i in sizes]
            
            titles=[c.title for c in lien_causes]
            pics=[c.icon_picture for c in lien_causes]
            colors=["grey" if c.secteur is None else 
                    c.secteur.color for c in lien_causes]
            text = [lien.cause_description for lien in causes]
            ids = [c.id for c in lien_causes]
            
            
            angle=[0]
            angle.extend([i+j for i,j in zip(sizes[:-1],sizes[1:])])
            angle=np.cumsum(angle)*(2*np.pi/(2*sum(sizes)))
            angle += np.pi - angle[-1]/2
            angle *= side_angle/2 
            angle += (1-side_angle)/2*np.pi + np.pi/2
            pos =  [(distance*np.cos(i),distance*np.sin(i)) for i in angle]
               
            # storing as object list 
            icons=[IconObj(*i) for i in 
                zip(titles,text,pics,colors,pos,sizes,ids)]
        else:
            icons=[]
        
        try:
            color_center=self.secteur.color 
        except AttributeError:
            color_center="grey"
        center = IconObj(self.title,self.short_description,
                            self.icon_picture,color_center,
                            (0,0),size_center,self.id)
                            

        con = self.consequences.all()
        
        if len(con)>0:
            # computing position and size of the graphic elements
            titles2 =[lien.consequence.title for lien in con]
            text2 = [lien.consequence_description for lien in con]
            pics2 =[lien.consequence.icon_picture for lien in con]
            colors2 =["grey" if lien.consequence.secteur is None else 
                    lien.consequence.secteur.color for lien in con]
            ids2 = [lien.consequence.id for lien in con]

            angle2=np.linspace(0,2*np.pi,len(con),endpoint=False)
            angle2 += np.pi - angle2[-1]/2
            angle2 *= side_angle/2 
            angle2 += (1-side_angle)/2*np.pi - 1/2*np.pi
            pos2 =  [(distance*np.cos(i),distance*np.sin(i)) for i in angle2]
            sizes2= [default_size]*len(con)
            
            # storing as object list 
            icons2=[IconObj(*i) for i in 
                zip(titles2,text2,pics2,colors2,pos2,sizes2,ids2)]
        else:
            icons2=[]
        
        pairs=[(i,center) for i in icons]
        pairs.extend([(center,i) for i in icons2])
        
        icons.extend(icons2)
        icons.append(center)
        
        if len(icons)==0:
            return False

        diag=DiagramObj("causes",icons,pairs,margin,width,height,line_width,
            text_size_factor=2)
        self.cause_diagram = diag
        return True
 
 
class Page(SujetOrSecteur):
    """ Subclass of <SujetOrSecteur> for storing page content """
    pass

    
### Serve content to the main classes ###

        
class Section(models.Model):
    """ Class to store a section of a webpage
    
    Attributes:
        title : <str> subtitle of the section (optionnal)
        section_text : 
        picture: <Picture> contains a picture and some metadata
        order : order of the section in the topic page
    """

    title = models.CharField(max_length=200, blank=True)
    subtitle = models.CharField(max_length=200, blank=True)
    text = models.TextField(default="", blank=True)
    
    order = models.PositiveSmallIntegerField()
    opinion = models.BooleanField(blank=True, default = False)
    background = models.ForeignKey(Picture, on_delete = models.SET_NULL,
        null = True, blank=True)
            
    sujet = models.ForeignKey(Sujet, on_delete = models.CASCADE,
        related_name = "section_set", null = True, blank=True)
    secteur = models.ForeignKey(Secteur, on_delete = models.CASCADE,
        related_name = "section_set", null = True, blank=True)
    page = models.ForeignKey(Page, on_delete = models.CASCADE,
        related_name = "section_set", null = True, blank=True)
    
    def __str__(self):
        s=""
        if self.sujet is not None:
            s = "Sujet: %s"%(self.sujet.name)
        elif self.secteur is not None:
            s = "Secteur: %s"%(self.secteur.name)
        elif self.page is not None:
            s = "Page: %s"%(self.page.name)
        max_len=25
        s="%s (%d) %s"%(s,self.order,self.title[:max_len])
        if len(self.title)>=max_len:
            s+="..."
        return s
    
    def get_text(self):
        res=[]
        last=False
        text=self.text
        if text=="":
            return text
        text=find_links(self.text)
        for i in text.split('\n'):
            boo=i[0]=='-'
            if boo:
                i = "\n<li> %s </li>"%i[1:]
            else:
                i = "\n" + i
            if not last and boo:               
                i = "\n</p><ul>" + i[1:]
            elif last and not boo:
                i = "\n</ul><p>" + i
            last=boo
                
            res.append(i)
        if last:
            res.append("</ul><p>")
        res = "".join(res)
        res=res.replace("\r\n","</p><p>")
        res=res.replace("\r","")
        res=res.replace("</p><p></p><p>","</p><br><p>")
        res=res.replace("</p><p></p><p>","</p><br><p>")
        return res
        
    def get_illustrations(self):
        """Order illustrations by pane position"""
        
        temp=[["L",[],0,0],["R",[],0,0],["center",[],0,0]]
        for pic in self.illustrations.all():
            
            if pic.position=="L":
                temp[0][1].append(pic)
                temp[0][2]=max(temp[0][2],pic.width)
                temp[0][3]+=pic.height
            elif pic.position=="R":
                temp[1][1].append(pic)
                temp[1][2]=max(temp[1][2],pic.width)
                temp[1][3]+=pic.height
            else:
                temp[2][1].append(pic)
                temp[2][2]+=pic.width
                temp[2][3]=max(temp[2][3],pic.height)
        temp[0][3]=max(temp[0][3],temp[1][3])
        temp[1][3]=temp[0][3]
        if len(temp[2][1])>0:
            pos = temp[2][1][0].position
            if pos == "BR":
                temp[2][0] = "right"
            elif pos == "BL":
                temp[2][0] = "left"
        self.text_size=(-temp[0][2]-temp[1][2],-temp[2][3])
        return temp


 
### Link topics together ###
        
        
class Lien(models.Model):
        """Class for storing a causality link between two Sujets:
        
        Attributes:
            cause: <Sujet> topics causing the other issue
            consequence: <Sujet> topics caused by the former issue
            relative_share: <float> between 0 and 100, quantifies 
                                          the impact this issue has on another
            description: <str> small text explaining the causality between both
        """
        cause = models.ForeignKey(Sujet,related_name="consequences",
                                        on_delete = models.CASCADE)
        consequence = models.ForeignKey(Sujet,related_name="causes",
                                        on_delete = models.CASCADE)
        relative_share = models.FloatField(default=None,blank=True, null=True)
        cause_description = models.CharField(max_length=400, blank=True)
        consequence_description = models.CharField(max_length=400, blank=True)
        
        def __str__(self):
            s="%s --> %s"%(self.cause.name,self.consequence.name)
            return s
            

 
### Illustration for some section
   
   
class Illustration(models.Model):
    name = models.CharField(max_length=50,default="Illustration")
    section = models.ManyToManyField(Section,related_name="illustrations")
    position = models.CharField(max_length=2,choices=POSITIONS, default="L")
    picture = models.ForeignKey(Picture, on_delete=models.SET_NULL, null=True, blank=True)
    code = models.TextField(null=True, blank=True)
    #nodes,arrows: set of graph nodes and arrows
    height = models.IntegerField()
    width = models.IntegerField()
    
    def picture_size(self):
        """return a resize factor for the picture if any"""
        w,h=self.width,self.height
        if self.picture is None:
            return False
        else: 
            size_pic,size_crop,margin_pic=self.picture.resize(width=w,height=h)
            self.size_pic = size_pic
            self.size_crop = size_crop
            self.margin_pic = margin_pic
        return True
    
    def get_diagram(self):
        """Returns a DiagramObj using nodes, liens and arrows"""
        self_nodes=self.nodes.all()
        self_arrows=self.arrows.all()
        
        
        if len(self_nodes)==0:
            return False
        
        nodes = [n.get_icon_obj() for n in self_nodes]
        node_liens = [n.liens.all() for n in self_nodes]
        
        pairs = []
        for n,n_liens in zip(nodes,node_liens):
            if len(n_liens)==0:
                    liens = Lien.objects.filter(cause__id=n.target_id).all()
                    liens = [l.consequence.id for l in liens]
                    temp = [(n,target) for target in nodes if target.target_id in liens]
                    pairs.extend(temp)
            else:
                ids=set([(i.cause.id,i.consequence.id) for i in n_liens])
                for n in nodes:
                    pairs.extend([(n,i) for i in nodes if i is not n and 
                                    (n.target_id,i.target_id) in ids])
        ids = set([(i.cause.id,i.consequence.id) for i in self_arrows])
        pairs = [p for p in pairs if (p[0].target_id,p[1].target_id) not in ids]
        
        lines=[]
        arrows=[]
        for obj in self_arrows:
            
            n0=[i for i in nodes if i.node_id==obj.cause.id]
            n1=[i for i in nodes if i.node_id==obj.consequence.id]
            if len(n0)!=1 or len(n1)!=1:
                continue
            n0=n0[0]
            n1=n1[0]
            
            pt=[(obj.X0, obj.Y0), (obj.X1,obj.Y1)]
            pt=[np.array(i) for i in pt if None not in i]
            if len(pt)==0:
                pairs.append((n0,n1))
                continue
            pairs = [p for p in pairs if (p[0].node_id,p[1].node_id)!=(n0.node_id,n1.node_id)]
            vect = pt[0]-np.array(n0.pos)
            first_pt = np.array(n0.pos)+vect*n0.size/np.sqrt(sum(vect*vect))
            vect = np.array(n1.pos) - pt[-1]
            last_pt = np.array(n1.pos)-vect*n1.size/np.sqrt(sum(vect*vect))
            pt=[first_pt,*pt,last_pt]
            
            lines.extend([((*i,*j),n0.color) for i,j in zip(pt[:-1],pt[1:])])
            arrows.append(((*pt[-2],*pt[-1]),n0.color))
            
        
        margin=10
        line_width=2
            
        diagram=DiagramObj(self.id,nodes,pairs,margin,
                            self.width,self.height,line_width)
        diagram.add_arrows(arrows,lines)
        print(diagram.lines)
        return diagram
    
            

class GraphNode(models.Model):
    """Stores the impact map nodes and arrows"""
    illustration = models.ForeignKey(Illustration, on_delete = models.CASCADE,
        related_name="nodes")
    sujet = models.ForeignKey(Sujet, on_delete = models.CASCADE,
        related_name="+")
    radius = models.FloatField()
    X = models.FloatField()
    Y = models.FloatField()
    
    # optional arguments
    secteur = models.ForeignKey(Secteur,on_delete = models.SET_NULL, 
        null=True, blank = True)
    liens = models.ManyToManyField(Lien, blank = True)
    
    def get_icon_obj(self):
        
        if self.secteur is None:
            secteur = self.sujet.secteur 
        else:
            secteur = self.secteur
        
        color= "grey" if secteur is None else secteur.color
        res = IconObj(self.sujet.title, "", 
            self.sujet.icon_picture, color, (self.X,self.Y), 
            self.radius, self.sujet.id, node_id=self.id)
        return res
        
    
    
class GraphArrow(models.Model):
    """Stores broken Arrows"""
    illustration = models.ForeignKey(Illustration, on_delete = models.CASCADE,
        related_name="arrows")
    cause = models.ForeignKey(GraphNode, on_delete = models.CASCADE,
        related_name = "+")
    consequence = models.ForeignKey(GraphNode, on_delete = models.CASCADE,
        related_name = "+")
    X0 = models.FloatField(null=True, blank=True)
    Y0 = models.FloatField(null=True, blank=True) 
    X1 = models.FloatField(null=True, blank=True)
    Y1 = models.FloatField(null=True, blank=True) 

   

    
    

    
    
    
    

    
    