# File management tools
A collection of tools for handling files in batch
## Lndir
    usage: lndir.py [-h] [-s | -c | -d] from_dir from_structure to_structure
    
    Batch copy, hardlink or symlink files using regex
    
    positional arguments:
      from_dir        The dir to copy from
      from_structure  Regex expression describing the structure of the files
      to_structure    Expression with {^N} describing the inputs
    
    optional arguments:
      -h, --help      show this help message and exit
      -s, --symlink   Create symlinks instead of hardlinks
      -c, --copy      Copy files instead of symlink
      -d, --dry       List the files that would be created

### Example 1: Basic usage
Given a directory structure
* /SeriesName
  * SeriesName_S01E01.mkv
  * SeriesName_S01E02.mkv
  * SeriesName_S02E01.mkv
```
./lndir.py -s /SeriesName "S(\d{2})E(\d{2})" /NewLocation/S{^1}/SeriesName_S{^1}E{^2}.mkv
```
will create a structure like this
* /NewLocation
  * S01
    * SeriesName_S01E01.mkv
    * SeriesName_S01E02.mkv
  * S02
    * SeriesName_S02E01.mkv
    
Where the folders will be created recursively, with the files themselves as symlinks.