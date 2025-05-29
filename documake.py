import sys
from bs4 import BeautifulSoup

def main():
  main_file_handle = None
  try:
    with open('test/main.html') as main_file:
      main_file_handle = BeautifulSoup(main_file, 'html.parser')
  except FileNotFoundError:
    print("Main file not found.")
    sys.exit(1)
  
  replace_targets = main_file_handle.find_all('a', attrs={'data-dmreplace': True})
  for target in replace_targets:
    try:
      target_contents = None
      with open('test/'+target['href']) as target_handle:
        target_contents = BeautifulSoup(target_handle, 'html.parser')
    except FileNotFoundError:
      print(f"replace file {'test/'+target['href']} not found.")
      sys.exit(1)
      
    target.replace_with(target_contents)

  with open('test/out.html', 'w') as output_handle:
    output_handle.write(main_file_handle.prettify())

    
if __name__ == "__main__":
  main()
