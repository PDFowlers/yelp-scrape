## -----

After cloning the repo and installing dependencies (and adding the .gitignore+Pipenv stuff), I ran the following command

(for reference, `pipenv run` uses the "pipenv" which is a dedicated Python environment just for this project, instead of running just `python -m ...` which uses the computer's default Python environment which is shared across ~everything)

`pipenv run python -m yelp_scrape -- food "South Lyon"`

This gave me the following error:

## Output

```
Usage: python -m yelp_scrape [OPTIONS] COMMAND [ARGS]...
Try 'python -m yelp_scrape --help' for help.
```

## -----

I guess I messed up the command format

so I tried getting help with `pipenv run python -m yelp_scrape -- --help` and got the following:

## Output

```
Usage: python -m yelp_scrape [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  yelp-scrape  yelp_scrape will run the full program.
```

## -----

Ah, I see, there is a subcommand called yelp-scrape, let me try that: `pipenv run python -m yelp_scrape -- yelp-scrape food "South Lyon"`

## Output

```
Traceback (most recent call last):
  File "C:\Users\riiza\AppData\Local\Programs\Python\Python310\lib\runpy.py", line 196, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "C:\Users\riiza\AppData\Local\Programs\Python\Python310\lib\runpy.py", line 86, in _run_code
    exec(code, run_globals)
  File "D:\Dev\yelp-scrape\yelp_scrape.py", line 84, in <module>
    cli()
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1130, in __call__
    return self.main(*args, **kwargs)
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1055, in main
    rv = self.invoke(ctx)
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1657, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1404, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 760, in invoke
    return __callback(*args, **kwargs)
  File "D:\Dev\yelp-scrape\yelp_scrape.py", line 77, in yelp_scrape
    yelp_soup: BeautifulSoup | str = local_cache_check(url, file_name, cache)
  File "D:\Dev\yelp-scrape\yelp_scrape.py", line 41, in local_cache_check
    file_list = os.listdir(f'{cache}')
FileNotFoundError: [WinError 3] The system cannot find the path specified: 'WebCache'
```

## -----

Dope! Progress!

`local_cache_check` tries to find `./WebCache/` but can't, because it doesn't exist.

This behavior seems undesired. If the cache doesn't exist, we want to create it automatically, not require our users to create it by hand before the program will run. Okay, let's do that.

We'll just add `cache.mkdir(exist_ok=True, parents=True)` to `local_cache_check()` to ensure the cache directory exists. (The parameters make sure that if it already exists, it doesn't throw an error, and if its parent directories don't exist, we'll go ahead and create those too).

Okay, now I'm ready to test again.

## Output

```
Writing new file in the directory
Traceback (most recent call last):
  File "C:\Users\riiza\AppData\Local\Programs\Python\Python310\lib\runpy.py", line 196, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "C:\Users\riiza\AppData\Local\Programs\Python\Python310\lib\runpy.py", line 86, in _run_code
    exec(code, run_globals)
  File "D:\Dev\yelp-scrape\yelp_scrape.py", line 86, in <module>
    cli()
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1130, in __call__
    return self.main(*args, **kwargs)
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1055, in main
    rv = self.invoke(ctx)
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1657, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1404, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 760, in invoke
    return __callback(*args, **kwargs)
  File "D:\Dev\yelp-scrape\yelp_scrape.py", line 79, in yelp_scrape
    yelp_soup: BeautifulSoup | str = local_cache_check(url, file_name, cache)
  File "D:\Dev\yelp-scrape\yelp_scrape.py", line 54, in local_cache_check
    file.write(yelp_soup)
TypeError: write() argument must be str, not BeautifulSoup
```

## -----

Okay, looks like I ran into the error I was telling you about a few comments ago. Let's check line 54 like it says.

Indeed, we're writing a BeautifulSoup object, which doesn't work.

We can change line 54 to write the original `response.content`, which is a `str`.

Let's try again.

## Output

```
Retrieving the file from the directory
```

## -----

Ah. I forgot to delete the empty cache file that was written because it opened the file, then died before writing anything. So now we're opening an empty file, which means nothing is going to happen. I'll just delete the cache file and try again.

## Output

```
Writing new file in the directory
Traceback (most recent call last):
  File "C:\Users\riiza\AppData\Local\Programs\Python\Python310\lib\runpy.py", line 196, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "C:\Users\riiza\AppData\Local\Programs\Python\Python310\lib\runpy.py", line 86, in _run_code
    exec(code, run_globals)
  File "D:\Dev\yelp-scrape\yelp_scrape.py", line 86, in <module>
    cli()
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1130, in __call__
    return self.main(*args, **kwargs)
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1055, in main
    rv = self.invoke(ctx)
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1657, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1404, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 760, in invoke
    return __callback(*args, **kwargs)
  File "D:\Dev\yelp-scrape\yelp_scrape.py", line 79, in yelp_scrape
    yelp_soup: BeautifulSoup | str = local_cache_check(url, file_name, cache)
  File "D:\Dev\yelp-scrape\yelp_scrape.py", line 54, in local_cache_check
    file.write(yelp_page.content)
TypeError: write() argument must be str, not bytes
```

## -----

My bad, `.content` gives a byte stream, we actually want `.text` which gives the `str`. I'll go ahead and make that fix, and delete the cache file again and rerun.

## Output

```
Writing new file in the directory
Traceback (most recent call last):
  File "C:\Users\riiza\AppData\Local\Programs\Python\Python310\lib\runpy.py", line 196, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "C:\Users\riiza\AppData\Local\Programs\Python\Python310\lib\runpy.py", line 86, in _run_code
    exec(code, run_globals)
  File "D:\Dev\yelp-scrape\yelp_scrape.py", line 86, in <module>
    cli()
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1130, in __call__
    return self.main(*args, **kwargs)
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1055, in main
    rv = self.invoke(ctx)
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1657, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1404, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 760, in invoke
    return __callback(*args, **kwargs)
  File "D:\Dev\yelp-scrape\yelp_scrape.py", line 80, in yelp_scrape
    yelp_soup: BeautifulSoup = BeautifulSoup(yelp_soup, 'html.parser')
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\bs4\__init__.py", line 312, in __init__
    markup = markup.read()
TypeError: 'NoneType' object is not callable
```

## -----

Okay, `yelp_soup` is `None`. Why?

We got it from the `local_cache_check` function, so let's see what's going on there.

The output confirms we hit the branch where there was no cache file, so we write the cache.

Then we return the `yelp_soup` object. Everything looks good to my eye in this function, so it looks like `BeautifulSoup(yelp_page.content, 'html.parser')` is returning `None`.

I think it's the same bug as earlier, we're giving it `yelp_page.content` (which is `bytes`) rather than `yelp_page.text` (which is `str`). I'd expect this to error, but for some reason it fails silently. Thanks, Python, dope feature.

Let's change it to `yelp_page.text` and see what happens. I also want to get rid of the cached page because we want to trigger this same branch again, we don't want to trigger the branch that reads from the cache file, since that behavior is different.

## Output

```
Writing new file in the directory
Traceback (most recent call last):
  File "C:\Users\riiza\AppData\Local\Programs\Python\Python310\lib\runpy.py", line 196, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "C:\Users\riiza\AppData\Local\Programs\Python\Python310\lib\runpy.py", line 86, in _run_code
    exec(code, run_globals)
  File "D:\Dev\yelp-scrape\yelp_scrape.py", line 86, in <module>
    cli()
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1130, in __call__
    return self.main(*args, **kwargs)
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1055, in main
    rv = self.invoke(ctx)
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1657, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1404, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 760, in invoke
    return __callback(*args, **kwargs)
  File "D:\Dev\yelp-scrape\yelp_scrape.py", line 80, in yelp_scrape
    yelp_soup: BeautifulSoup = BeautifulSoup(yelp_soup, 'html.parser')
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\bs4\__init__.py", line 312, in __init__
    markup = markup.read()
TypeError: 'NoneType' object is not callable
```

## -----

Well, I was wrong. I guess BeautifulSoup can read bytes just fine. I was looking in the wrong place. I just glossed over the line in the error that said `File "D:\Dev\yelp-scrape\yelp_scrape.py", line 80, in yelp_scrape`.

So let's look at the line that actually generated the error in the first place.

I see, we return a BeautifulSoup object from `local_cache_check`, then we try to parse it again, which doesn't work. Let's just remove that code and assume `local_cache_check` returns a `BeautifulSoup` object (because for this branch at least, it does).

I'll delete the cached file and run once again.

## Output

```
Writing new file in the directory
/
#
/advertise/consumer_header_redirect
/writeareview
/login?return_url=https://www.yelp.com/search?find_desc=food&find_loc=South+Lyon
/signup?return_url=https://www.yelp.com/search?find_desc=food&find_loc=South+Lyon
/search?cflt=restaurants&find_loc=South%20Lyon
/search?cflt=homeservices&find_loc=South%20Lyon
/search?cflt=auto&find_loc=South%20Lyon
Traceback (most recent call last):
  File "C:\Users\riiza\AppData\Local\Programs\Python\Python310\lib\runpy.py", line 196, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "C:\Users\riiza\AppData\Local\Programs\Python\Python310\lib\runpy.py", line 86, in _run_code
    exec(code, run_globals)
  File "D:\Dev\yelp-scrape\yelp_scrape.py", line 85, in <module>
    cli()
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1130, in __call__
    return self.main(*args, **kwargs)
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1055, in main
    rv = self.invoke(ctx)
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1657, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1404, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 760, in invoke
    return __callback(*args, **kwargs)
  File "D:\Dev\yelp-scrape\yelp_scrape.py", line 80, in yelp_scrape
    pages: list = collect_webpages(yelp_soup)
  File "D:\Dev\yelp-scrape\yelp_scrape.py", line 63, in collect_webpages
    print(a['href'])
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\bs4\element.py", line 1519, in __getitem__
    return self.attrs[key]
KeyError: 'href'
```

## -----

Voila! Now we're getting further in the code.

Okay, let's just run once more, this time _without_ deleting the cache file, to ensure that branch also works. (I suspect it won't).

## Output

```
Retrieving the file from the directory
Traceback (most recent call last):
  File "C:\Users\riiza\AppData\Local\Programs\Python\Python310\lib\runpy.py", line 196, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "C:\Users\riiza\AppData\Local\Programs\Python\Python310\lib\runpy.py", line 86, in _run_code
    exec(code, run_globals)
  File "D:\Dev\yelp-scrape\yelp_scrape.py", line 85, in <module>
    cli()
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1130, in __call__
    return self.main(*args, **kwargs)
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1055, in main
    rv = self.invoke(ctx)
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1657, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1404, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 760, in invoke
    return __callback(*args, **kwargs)
  File "D:\Dev\yelp-scrape\yelp_scrape.py", line 80, in yelp_scrape
    pages: list = collect_webpages(yelp_soup)
  File "D:\Dev\yelp-scrape\yelp_scrape.py", line 62, in collect_webpages
    for a in soup.find_all('a'):
AttributeError: 'str' object has no attribute 'find_all'
```

## -----

Indeed, when we read from the cache file, we return the `str` directly. `local_cache_check` _says_ it returns a `BeautifulSoup` object, but that's a damned dirty lie at the moment. Let's fix that to make sure it always returns a `BeautifulSoup` object by parsing the text after it reads the cache file.

And we can keep the cache file, and run again to test.

## Output

```
Retrieving the file from the directory
/
#
/advertise/consumer_header_redirect
/writeareview
/login?return_url=https://www.yelp.com/search?find_desc=food&find_loc=South+Lyon
/signup?return_url=https://www.yelp.com/search?find_desc=food&find_loc=South+Lyon
/search?cflt=restaurants&find_loc=South%20Lyon
/search?cflt=homeservices&find_loc=South%20Lyon
/search?cflt=auto&find_loc=South%20Lyon
Traceback (most recent call last):
  File "C:\Users\riiza\AppData\Local\Programs\Python\Python310\lib\runpy.py", line 196, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "C:\Users\riiza\AppData\Local\Programs\Python\Python310\lib\runpy.py", line 86, in _run_code
    exec(code, run_globals)
  File "D:\Dev\yelp-scrape\yelp_scrape.py", line 86, in <module>
    cli()
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1130, in __call__
    return self.main(*args, **kwargs)
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1055, in main
    rv = self.invoke(ctx)
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1657, in invoke
    return _process_result(sub_ctx.command.invoke(sub_ctx))
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 1404, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\click\core.py", line 760, in invoke
    return __callback(*args, **kwargs)
  File "D:\Dev\yelp-scrape\yelp_scrape.py", line 81, in yelp_scrape
    pages: list = collect_webpages(yelp_soup)
  File "D:\Dev\yelp-scrape\yelp_scrape.py", line 64, in collect_webpages
    print(a['href'])
  File "C:\Users\riiza\.virtualenvs\yelp-scrape-rBWDAnfj\lib\site-packages\bs4\element.py", line 1519, in __getitem__
    return self.attrs[key]
KeyError: 'href'
```

## -----

Great! We're in the same place for both branches. I'd like to refactor `local_cache_check`, but for now, let's move on.

Looks like we're fetching all `a` tags and printing their `href` attribute. That makes sense. Apparently though, at least one of them doesn't have an `href` attribute. What the fuck, Yelp?

Okay, let's change the print statement to get a little more information.

Unfortunately, I don't know what type `a` is because it's a little hidden, so I don't know what information I can get from the object. Let's first get a `print(type(a))` so I can look at the BeautifulSoup documentation and see what info I can get

## Output

```
Retrieving the file from the directory
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
<class 'bs4.element.Tag'>
```

## -----

That's a lot of tags. Okay, let's google "BeautifulSoup docs", which gets us https://www.crummy.com/software/BeautifulSoup/bs4/doc/

There's no search function, so I'll just ctrl+f for "tag".

Great, there's a section that describes them briefly. It doesn't list everything, which kind of sucks, but that's fine. Now I know there's an `attrs` field. Let's try:

```python
print("-----")
print(a)
print(a.attrs)
print("-----")
```

I added the `-----` to clearly separate each iteration from the others, so it's a bit more readable.

But wait, there were a ton of tags. We only really want to investigate the ones we're interested in, the ones without an `href`. The docs say we can treat a `Tag` as if it's a dictionary, so let's modify our prints to the following:

```python
if not 'href' in a:
    print("-----")
    print(a)
    print(a.attrs)
    print("-----")
```

## Output (truncated)

```
...
-----
<a class="css-cv1jz2" href="https://www.yelp.com/tos/privacy_policy">Privacy Policy</a>
{'href': 'https://www.yelp.com/tos/privacy_policy', 'class': ['css-cv1jz2']}
-----
-----
<a class="css-1um3nx" href="http://databyacxiom.com" rel="nofollow" target="_blank">Some Data By Acxiom</a>
{'href': 'http://databyacxiom.com', 'class': ['css-1um3nx'], 'target': '_blank', 'rel': ['nofollow']}
-----
```

## -----

The docs lied to us. We can't treat `Tag` like a dictionary. So let's just use the `attrs` dict directly and try:

```python
if not 'href' in a.attrs:
    print("-----")
    print(a)
    print(a.attrs)
    print("-----")
```

## Output

```
Retrieving the file from the directory
-----
<a class="header-link_anchor__09f24__eCD4u default-cursor__09f24__E8P1i" tabindex="0"><span class="css-qgunke">More</span><span class="display--inline__09f24__c6N_k padding-l0-5__09f24__tBn3z border-color--default__09f24__NPAKY"><span alt="" aria-hidden="true" class="icon--24-chevron-down-v2 css-147xtl9" role="img"><svg class="icon_svg" height="24" width="24"><path d="M12 15.25a1 1 0 01-.7-.29l-4.58-4.5A1.011 1.011 0 018.12 9L12 12.85 15.88 9a1 1 0 111.4 1.42L12.7 15a1 1 0 01-.7.25z"></path></svg></span></span></a>
{'class': ['header-link_anchor__09f24__eCD4u', 'default-cursor__09f24__E8P1i'], 'tabindex': '0'}
-----
-----
<a class="header-link_anchor__09f24__eCD4u default-cursor__09f24__E8P1i" tabindex="0"><span class="css-qgunke">More</span><span class="display--inline__09f24__c6N_k padding-l0-5__09f24__tBn3z border-color--default__09f24__NPAKY"><span alt="" aria-hidden="true" class="icon--24-chevron-down-v2 css-147xtl9" role="img"><svg class="icon_svg" height="24" width="24"><path d="M12 15.25a1 1 0 01-.7-.29l-4.58-4.5A1.011 1.011 0 018.12 9L12 12.85 15.88 9a1 1 0 111.4 1.42L12.7 15a1 1 0 01-.7.25z"></path></svg></span></span></a>
{'class': ['header-link_anchor__09f24__eCD4u', 'default-cursor__09f24__E8P1i'], 'tabindex': '0'}
-----
```

## -----

Much more reasonable. These to me look like some weird auto-generated JavaScript bullshit that have something to do with page layout. They're coded as links for who knows what reason, but they don't actually take you to a URL, they just open menus or some shit.

Well, okay. But now we know how to filter out tags without `href`, so we may as well do that to grab the set of tags we're interested in. I'll modify the function to the following:

```python
for a in soup.find_all('a'):
    if 'href' in a.attrs:
        print("do something")
```

Now we have a clear point of continuation. We're now guaranteed that any "a" tag under that if statement has an `href` attribute.
