import local
import file_io as fi

if __name__ == "__main__":
	with open("hdlines.txt", "w+") as w:
		print local.news_dir
		for f in fi.getTopLevelFiles(local.news_dir):
			f = f.split("\\")[-1]
			if f.endswith("WIRED.htm"):
				f = '<h1 id="post-title">' + f.replace(' _ WIRED.htm', '') + '</h1>'
			elif f.endswith("CNN.com.htm"):
				f = '<h1 class="pg-headline">' + f.replace(' - CNN.com.htm', '') + '</h1>'
			elif f.endswith("VICE News.htm"):
				f = '<h1 class="article-title">' + f.replace(' _ VICE News.htm', '') + '</h1>'
			else:
				continue
			w.write(f + '\n')