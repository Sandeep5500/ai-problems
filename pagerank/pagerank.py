import os
import random
import re
import sys
import copy
import itertools

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probs = {}
   
    nlinks = len(corpus[page])
    npages = len(corpus)

    if corpus[page] == set():
        for webpage in corpus:
            probs[webpage] = 1/npages
    else:             
        for link_page in corpus[page]:
            probs[link_page]=damping_factor/nlinks   
        for webpage in corpus:
            if webpage in probs:
                probs[webpage] = probs[webpage]+ (1-damping_factor)/npages
            else:
                probs[webpage] = (1-damping_factor)/npages         
    
    return probs


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    start = random.choice(list(corpus.keys()))
    probs = transition_model(corpus,start,damping_factor)
    ranks = {key: 0 for key in list(corpus.keys())} 

    for i in range(n):
        page = random.choices(list(probs.keys()), list(probs.values()))
        ranks[page[0]] = ranks[page[0]] + 1
        probs = transition_model(corpus,page[0],damping_factor)

    ranks = {k: v / n for k, v in ranks.items()}
    return ranks

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    n = len(corpus)
    ranks = {key: 1/n for key in list(corpus.keys())}
    temp_ranks = copy.deepcopy(ranks)
    done = False

    # print(f"{corpus}")

    for page in corpus:
        if corpus[page] == set():
            corpus[page] = set(corpus.keys())
    # print(f"{corpus}")

    while(done == False):
        for page in corpus:    
            temp_ranks[page] = (1-damping_factor)/n
            nolinks = True
            for pagek in corpus:
                if page in corpus[pagek]:
                    nolinks = False
                    temp_ranks[page] = temp_ranks[page] + damping_factor*((ranks[pagek])/len(corpus[pagek]))  
            
        # print (f"{temp_ranks}")            
        done = True
        for page in ranks:
            if ranks[page] - temp_ranks[page] > 0.0001:
                done = False
                break
        if done == True:
            break
        ranks = copy.deepcopy(temp_ranks)    
         
    return ranks           


if __name__ == "__main__":
    main()
