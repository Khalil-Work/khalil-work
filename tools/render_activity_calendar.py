"""Render recorded GitHub counts with fixed, explicit intensity thresholds.

This changes only a profile SVG. It never creates or modifies Git history.
Usage: python tools/render_activity_calendar.py
"""
import argparse
import datetime as dt
import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)
COLORS = {'none':'#edf1f5', 'low':'#b9e6c7', 'medium':'#43b66d', 'high':'#087f5b'}


def band(count):
    if count == 0:
        return 'none'
    if count <= 2:
        return 'low'
    if count <= 9:
        return 'medium'
    return 'high'


def render(source, output):
    data = json.loads(source.read_text(encoding='utf-8'))
    days = data['days']
    dates = [dt.date.fromisoformat(d['date']) for d in days]
    counts = [d['count'] for d in days]
    if not days or len(set(dates)) != len(dates) or dates != sorted(dates):
        raise ValueError('Dates must be nonempty, unique and sorted')
    if any(type(c) is not int or c < 0 for c in counts):
        raise ValueError('Counts must be nonnegative integers')
    if sum(counts) != data['total_contributions']:
        raise ValueError('Recorded total does not match the individual counts')
    if len(days) != (dates[-1]-dates[0]).days+1:
        raise ValueError('The snapshot must contain every date in its range')
    sunday = dates[0] - dt.timedelta(days=(dates[0].weekday()+1)%7)
    columns = (dates[-1]-sunday).days//7 + 1
    if columns > 54:
        raise ValueError('This layout supports up to54 calendar weeks')
    width, height = 1140, 342
    root = ET.Element(f'{{{SVG}}}svg', {'viewBox':f'0 0 {width} {height}', 'width':str(width), 'height':str(height), 'role':'img', 'aria-labelledby':'title description'})
    ET.SubElement(root, f'{{{SVG}}}title', {'id':'title'}).text = '2026 contribution-count snapshot with fixed low, medium and high thresholds'
    ET.SubElement(root, f'{{{SVG}}}desc', {'id':'description'}).text = 'Counts are recorded from GitHub. Low is1–2, medium3–9 and high10+ contributions per day. Historical counts include explicitly disclosed calendar-reconstruction records. This is a separate profile card, not the native GitHub graph.'
    ET.SubElement(root, f'{{{SVG}}}rect', {'width':str(width), 'height':str(height), 'rx':'16', 'fill':'#ffffff'})
    def text(x, y, value, size=14, color='#526274', **attrs):
        element=ET.SubElement(root, f'{{{SVG}}}text', {'x':str(x), 'y':str(y), 'font-family':'Arial, sans-serif', 'font-size':str(size), 'fill':color, **attrs})
        element.text=value
    text(32, 39, '2026 activity calendar', 24, '#172e46', **{'font-weight':'700'})
    text(32, 65, 'Fixed intensity scale · contribution counts per day', 14)
    active=sum(c>0 for c in counts)
    text(1108, 38, f'{sum(counts)} contributions', 21, '#172e46', **{'text-anchor':'end', 'font-weight':'700'})
    text(1108, 64, f'{active} active days / {len(days)} dates', 14, **{'text-anchor':'end'})
    grid_x, grid_y, pitch, cell = 92, 112, 18, 14
    text(32, 137, 'Mon', 12)
    text(32, 173, 'Wed', 12)
    text(32, 209, 'Fri', 12)
    month_seen=set()
    day_bands={name:0 for name in COLORS}
    for date,count in zip(dates,counts):
        col=(date-sunday).days//7
        row=(date.weekday()+1)%7
        if date.month not in month_seen:
            text(grid_x+pitch*col, 97, date.strftime('%b'), 12)
            month_seen.add(date.month)
        level=band(count)
        day_bands[level]+=1
        rect=ET.SubElement(root, f'{{{SVG}}}rect', {'x':str(grid_x+col*pitch), 'y':str(grid_y+row*pitch), 'width':str(cell), 'height':str(cell), 'rx':'3', 'fill':COLORS[level]})
        ET.SubElement(rect, f'{{{SVG}}}title').text=f'{date.isoformat()}: {count} contributions — {level}'
    for x,key,label in [(92,'none','None · 0'),(280,'low','Low · 1–2'),(468,'medium','Medium · 3–9'),(690,'high','High · 10+')]:
        ET.SubElement(root, f'{{{SVG}}}rect', {'x':str(x), 'y':'253', 'width':'16', 'height':'16', 'rx':'3', 'fill':COLORS[key]})
        text(x+24,266,label,13,'#172e46')
    labels=[f'{name.title()}: {day_bands[name]} '+('day' if day_bands[name]==1 else 'days') for name in ('low','medium','high')]
    text(92,292,'    '.join(labels),12)
    text(32,316,f'Snapshot: {data["snapshot_local"]}. Source: GitHub; historical counts include disclosed reconstruction records.',11)
    text(32,333,'This fixed-scale profile card is separate from GitHub’s automatic contribution graph.',11)
    output.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(output, encoding='utf-8', xml_declaration=True)
    return {'days':len(days),'total':sum(counts),'bands':day_bands,'output':str(output)}


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input',type=Path,default=ROOT/'data/contributions-2026.json')
    parser.add_argument('--output',type=Path,default=ROOT/'media/activity-2026.svg')
    args=parser.parse_args()
    print(json.dumps(render(args.input,args.output),indent=2))
