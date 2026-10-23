#!/usr/bin/env python3
"""Deterministic, dependency-light studio renderer. No generative media models."""
import json,sys,subprocess,tempfile,math,random,textwrap
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
job=json.loads(Path(sys.argv[1]).read_text()); output=Path(sys.argv[2]); output.parent.mkdir(parents=True,exist_ok=True)
studio=job['studio']; vertical=job['format']=='short'; W,H=(540,960) if vertical else (960,540); FPS=24
COLORS={'kinetic':('#10101d','#b9ff66'),'atlas':('#071f2e','#47d7ed'),'sketch':('#f5f0e8','#292b38'),'pixelverse':('#1b1737','#f6b655'),'chatdrama':('#10151f','#8c80ff')};bg,accent=COLORS[studio]
fontpath='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf';fontreg='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
if not Path(fontpath).exists():
 from PIL import __file__ as pilfile
 fontpath=str(Path(pilfile).parent/'fonts/DejaVuSans.ttf');fontreg=fontpath
font=lambda size,bold=True:ImageFont.truetype(fontpath if bold else fontreg,max(10,int(size)))
def textwrap_pixels(draw,s,maxw,f):
 words=s.split();lines=[];line=''
 for word in words:
  test=(line+' '+word).strip()
  if draw.textbbox((0,0),test,font=f)[2]>maxw and line:lines.append(line);line=word
  else:line=test
 if line:lines.append(line)
 return lines[:8]
def centered(draw,s,y,f,color,maxw):
 lines=textwrap_pixels(draw,s,maxw,f);spacing=f.size*1.32
 for i,line in enumerate(lines):
  draw.text((W/2,y+i*spacing),line,font=f,fill=color,anchor='mt',stroke_width=0)
 return y+len(lines)*spacing

def draw_frame(scene,index,total,progress):
 im=Image.new('RGB',(W,H),bg);d=ImageDraw.Draw(im);rng=random.Random(index*971+42)
 margin=int(W*.08); d.rounded_rectangle((margin,35,W-margin,42),radius=4,fill='#343847');d.rounded_rectangle((margin,35,margin+(W-2*margin)*(index+progress)/total,42),radius=4,fill=accent)
 if studio=='kinetic':
  for k in range(9):
   x=(k*127+index*31)%W;y=(k*181+index*59)%H
   d.ellipse((x,y,x+3+k%4,y+3+k%4),fill='#333348')
  size=round(min(W*.094,55)); y=H*.27
  centered(d,scene['title'].upper(),y,font(size),accent,W*.86)
  d.rounded_rectangle((W*.15,H*.45,W*.85,H*.45+5),radius=3,fill=accent)
  centered(d,scene['body'],H*.53,font(min(W*.047,30),False),'#ffffff',W*.82)
 elif studio=='atlas':
  centered(d,scene['title'],H*.16,font(W*.055),accent,W*.85)
  values=[rng.randint(22,85) for _ in range(5)];base=H*.68
  for k,val in enumerate(values):
   x=W*(.15+k*.15);bh=val/100*H*.38
   d.rounded_rectangle((x,base-bh,x+W*.09,base),radius=7,fill=accent if k==index%5 else '#28566a')
   d.text((x+W*.045,base+15),str(k+1),font=font(15,False),fill='#a9dce4',anchor='mt')
  centered(d,scene['body'],H*.78,font(W*.034,False),'#ffffff',W*.85)
 elif studio=='sketch':
  d.rounded_rectangle((margin,H*.13,W-margin,H*.85),radius=24,outline='#aaa4a0',width=3)
  cx=W*.5;cy=H*.48;head=W*.065
  d.ellipse((cx-head,cy-head*2.5,cx+head,cy-head*.5),outline=accent,width=5)
  d.line((cx,cy-head*.5,cx,cy+head*2),fill=accent,width=6)
  d.line((cx,cy+head*.2,cx-head*1.6,cy+head),fill=accent,width=5)
  d.line((cx,cy+head*.2,cx+head*1.6,cy+head*.5),fill=accent,width=5)
  d.line((cx,cy+head*2,cx-head*1.2,cy+head*3.6),fill=accent,width=5)
  d.line((cx,cy+head*2,cx+head*1.2,cy+head*3.6),fill=accent,width=5)
  centered(d,scene['title'],H*.19,font(W*.053),accent,W*.78)
  centered(d,scene['body'],H*.74,font(W*.032,False),accent,W*.76)
 elif studio=='pixelverse':
  px=max(8,W//60)
  for k in range(55):
   x=rng.randrange(0,W//px)*px;y=rng.randrange(0,int(H*.65)//px)*px
   d.rectangle((x,y,x+px//2,y+px//2),fill='#5c547e')
  for k in range(W//px+1):
   x=k*px;h=int(H*.76+math.sin(k*.38)*H*.04)
   d.rectangle((x,h,x+px,H),fill='#39415a' if k%2 else '#303952')
  x=int(W*.46);y=int(H*.65+math.sin(progress*math.pi*2)*6)
  d.rectangle((x-2*px,y-5*px,x+2*px,y),fill='#f6b655');d.rectangle((x-px,y-7*px,x+px,y-5*px),fill='#e9a3a2');d.rectangle((x-2*px,y,x-px,y+2*px),fill='#93c3e2');d.rectangle((x+px,y,x+2*px,y+2*px),fill='#93c3e2')
  centered(d,scene['title'],H*.16,font(W*.055),accent,W*.87)
  d.rounded_rectangle((margin,H*.8,W-margin,H*.93),radius=10,fill='#0d1024',outline=accent,width=2)
  centered(d,scene['body'],H*.83,font(W*.031,False),'#ffffff',W*.79)
 else:
  d.rounded_rectangle((margin,H*.14,W-margin,H*.88),radius=25,fill='#1b2431')
  d.ellipse((margin+20,H*.18,margin+58,H*.18+38),fill=accent)
  d.text((margin+72,H*.18+18),'Unknown contact',font=font(W*.035),fill='#ffffff',anchor='lm')
  d.line((margin+20,H*.25,W-margin-20,H*.25),fill='#303b4d',width=2)
  d.rounded_rectangle((margin+22,H*.32,W-margin-55,H*.49),radius=19,fill='#313c50')
  centered(d,scene['title'],H*.36,font(W*.042), '#ffffff',W*.65)
  d.rounded_rectangle((margin+55,H*.56,W-margin-22,H*.76),radius=19,fill='#453f81')
  centered(d,scene['body'],H*.59,font(W*.032,False),'#ffffff',W*.64)
 d.text((W/2,H-28),'FRAMEFORGE  /  '+studio.upper(),font=font(12,False),fill=accent,anchor='mm')
 return im
with tempfile.TemporaryDirectory(prefix='frameforge_') as tmp:
 clips=[]
 for idx,scene in enumerate(job['scenes']):
  frame=draw_frame(scene,idx,len(job['scenes']),1);image=Path(tmp)/f'scene_{idx:03d}.png';frame.save(image)
  clip=Path(tmp)/f'clip_{idx:03d}.mp4';dur=float(scene.get('duration',3.5));
  cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-loop','1','-framerate',str(FPS),'-i',str(image),'-f','lavfi','-i','anullsrc=channel_layout=stereo:sample_rate=44100','-t',str(dur),'-c:v','libx264','-preset','ultrafast','-crf','26','-pix_fmt','yuv420p','-c:a','aac','-shortest',str(clip)]
  subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE);clips.append(clip)
 concat=Path(tmp)/'concat.txt';concat.write_text(''.join("file '"+str(p)+"'\n" for p in clips))
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(output)],check=True)
print(output)
