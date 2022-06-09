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

Hm... it looks like we're reusing yelp_soup. It contains BOTH the HTML text after the response, and then later it contains the parsed BeautifulSoup object. This is pretty confusing, since whether `yelp_soup` is a `str` or a `BeautifulSoup` depends on when we access it, and we also lose access to the original `str` response. Let's separate this into two variables, `response_text`, and `response_soup`.
