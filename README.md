# MC Info
Gathers Minecraft username information. 

# Usage
```bash
$ python3 mcinfo.py [-h] [-v] name [name ...]
```
Outputs name histories by default, more information when `-v` flag is used. 

# Output Format
```
##### Username: <username>
### Histories: 
<list of name histories>

### Extras:
UUID:     <uuid>
Migrated: <yes/no>
Skin URL: <url of skin>
Cape URL: <url of cape>
```

