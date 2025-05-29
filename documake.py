import sys

import argparse
from pathlib import Path

from bs4 import BeautifulSoup

def insert_snippet(soup, root):
  replace_targets = soup.find_all('a', attrs={'data-dminsert': True})
  for target in replace_targets:
    target_path = (root / target['href']).resolve()

    if not target_path.exists():
      print(f'Linked file {target_path} not found, skipping')
      continue

    target_contents = target_path.read_text()
    target_soup = BeautifulSoup(target_contents, 'html.parser')
    
    if target_soup.style is not None:
      soup.style.append(target_soup.style.extract().string)

    target.replace_with(target_soup)
    

def prepare_root(soup):
  if soup.head is None:
    head = soup.new_tag('head')
    soup.html.insert(0, head)
  
  if soup.head.find('style') is None:
    style = soup.new_tag('style')
    soup.head.append(style)


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('root_file_path', type=Path)
  parser.add_argument('output_file_path', type=Path)
  return parser.parse_args()


def main():
  args = parse_args()

  if not args.root_file_path.exists():
    print(f'Root file {args.root_file_path} does not exist')
    sys.exit(1)
  
  args.output_file_path.parent.mkdir(parents=True, exist_ok=True)

  html = args.root_file_path.read_text()
  soup = BeautifulSoup(html, 'html.parser')
  prepare_root(soup)
  insert_snippet(soup, args.root_file_path.parent)
  args.output_file_path.write_text(str(soup))


if __name__ == "__main__":
  main()
