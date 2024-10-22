
import hyperSel
import time
import hyperSel.general_utilities
import requests
from bs4 import BeautifulSoup
import re

def name_comma_flipper(name):
    try:
        name_list = name.split(",")
        new_name = f""

        length = len(name_list)
        for i in range(length - 1, -1, -1):     # Iterate through the array in reverse
            # print(name_list[i])
            new_name += f"{name_list[i]} "


        cleaned_string = re.sub(r'\s+', ' ', new_name).strip() # get ri dof extra spaces
        return cleaned_string
    except:
        return name

def guten_name_paren_swapper(name):
    try:
        #print("===========")
        #print(f"original: {name}")
        
        pattern = r'\((.*?)\)' # content in paren
        paren = re.findall(pattern, name)[0]
        # print("paren   :",paren)

        # remove paren content
        original_name_without_paren = name.replace(paren, "").replace("()", "").replace(".", "")
        # print("original_name_without_paren:", original_name_without_paren)
        
        # split paren content by space
        paren_names = paren.split(" ")
        names_to_swap = []
        for name in paren_names:
            if name in original_name_without_paren:
                continue
            else:
                names_to_swap.append(name)
        
        filtered_list = original_name_without_paren.split(" ")
        name_split_by_space = [item for item in filtered_list if item != '']

        #print("name_split_by_space  :", name_split_by_space)
        #print("names_to_swap        :", names_to_swap)

        new_array = replace_character_in_first_array(array1=name_split_by_space, array2=names_to_swap)
        full_name = ' '.join(new_array)
        
        return full_name
    except:
        return name

def replace_character_in_first_array(array1, array2):
    # Create a dictionary with the first character as the key and the item as the value from array2
    replacement_dict = {}
    for item in array2:
        first_char = item[0]
        replacement_dict[first_char] = item

    # Replace characters in array1 with the corresponding items from the replacement_dict
    new_array = []
    for item in array1:
        if item in replacement_dict:
            new_array.append(replacement_dict[item])
        else:
            new_array.append(item)

    return new_array

def get_author_of_book_grom_link(ebook_link):
    print("ebook_link:", ebook_link)

    response = requests.get(ebook_link)
    soup = BeautifulSoup(response.content, 'html.parser')

    return "baby"

def fix_title(temp_title):
    allowed_chars = 'abcdefghijklmnopqrstuvwxyz0123456789 .-_'
    return ''.join(c for c in temp_title if c.isalnum() or c.isspace() or c in allowed_chars)

def fix_desc(temp_description):
    desc = ''.join((e for e in temp_description
                    if e.isalnum() or e.isspace() and e not in ["'", '"', ',', '(', ')', '``', '`', '\\', "'", '"', ',', '_', '*', '~', '[', ']', '{', '}', ';', '+', '=', '?', '<', '>', '&', '|', '$', '#', '%', '^']))
    return desc

def fix_name(name):
    replace_empty = ["``", "`","\\", "'",'"', ".", ",", "_", "*", "~", "[", "]", "{", "}", ";", ":", "/", "+", "=", "?", "<", ">", "&", "|", "$", "#", "@", "%", "^","0", "1","2", "3","4", "5","6", "7","8","9", "0"]
    replace_space = ["[", "]", "{", "}", ";", ":", "/", "+", "=", "?", "<", ">", "&", "|", "$", "#", "@", "%", "^"]
    
    # Replace characters with empty string
    for char in replace_empty:
        name = name.replace(char, "")
    
    # Replace characters with space
    for char in replace_space:
        name = name.replace(char, " ")
    
    # Remove extra spaces and capitalize each word
    name = " ".join(name.split()).title()
    
    name = filter_formalities(name)
    name = remove_special_characters_from_ends(input_string=name)
    name = name.strip()
    return name



def remove_special_characters_from_ends(input_string):
    # Define the pattern to match special characters at the beginning and end of the string
    pattern = r'^[\W_]+|[\W_]+$'

    # Use regular expression to remove special characters from the beginning and end
    cleaned_string = re.sub(pattern, '', input_string)

    return cleaned_string

def filter_formalities(name):
    formalities = [
                    'Dr', 'Mr', 
                    'Mrs', 'PhD', 
                    'MSC','Dr.', 
                    'Mr.', 'Mrs.', 
                    'PhD.', 'MSC.', 
                    'Sir', 'Sir.',
                    'Prof.','Prof',
                    'Hon.','Hon',
                    'Rev','Rev.',
                    'Col.','Col',
                    'Pres.','Pres',
                    'Cfa.','Cfa',
                    'Md.','Md',
                    'Fr.','Fr',
                    'Congresswoman','Congressman',
                   ]  # List of basic formalities
    name_parts = name.split()  # Split the name string into a list of words
    cleaned_name_parts = []
    for i, part in enumerate(name_parts):
        if i == 0 and part in formalities:
            continue  # Skip formality word at the beginning of name
        cleaned_name_parts.append(part)
    cleaned_name = ' '.join(cleaned_name_parts)  # Join the remaining words into a cleaned name string
    return cleaned_name

def get_gutenberg_content_from_soup(soup):
    posts = []
    # print("get_gutenberg_content_from_soup", len(soup))
    list_of_items = soup.find("div", class_="pgdbbytitle")
   
    all_h2 = list_of_items.find_all("h2")
    all_p = list_of_items.find_all("p")

    count = 0
    for h2, p in zip(all_h2, all_p):
        if count > 100:
            break

        title = h2.find("a").text
        print("title", title)

        link = h2.find("a")["href"]
        link_id = link.split("/")[-1]
        ebook_link = f"https://www.gutenberg.org/ebooks/{link_id}"
        author = get_author_of_book_grom_link(ebook_link)
        print("author", author)

        author = p.find("a").text
        switched_name = name_comma_flipper(author)
        swap_name = guten_name_paren_swapper(switched_name)
        name_no_period = swap_name.replace(".", "")
        name_fixed = fix_name(name_no_period)
        print("name_fixed", name_fixed)
        
        # posts.append([title, title, url, "gutenberg", name_fixed])
        
        count +=1
        
    return posts

def gutenberg_thread():
    alphabet = hyperSel.general_utilities.get_all_alphabet_chars()

    for char in alphabet: # redtube only has this many 
        start = time.time()

        print(f"char: {char}")

        link = f"https://www.gutenberg.org/browse/titles/{char}"
        print("link:", link)

        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')

        posts = get_gutenberg_content_from_soup(soup)

        for i in range(50):
            print(posts[i])

        # db.group_insert(posts)
        # colors.logging_print_color(color="dark_purple", text_to_color="gutenberg", pre_text=F"DONE [{db.count_all_posts()}][NUM:{len(posts)}]", post_text=F"[{round(time.time() - start, 2)}]")

        break

if __name__ == '__main__':
    print("hello world")
