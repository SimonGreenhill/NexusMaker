# NexusMaker

## Simply Generate Nexus Files

```
from nexusmaker import NexusMaker, Record


data = [
    Record(Language="A", Parameter="eye", Item="", Cognacy="1"),
    Record(Language="A", Parameter="leg", Item="", Cognacy="1"),
    Record(Language="A", Parameter="arm", Item="", Cognacy="1"),
    
    Record(Language="B", Parameter="eye", Item="", Cognacy="1"),
    Record(Language="B", Parameter="leg", Item="", Cognacy="2"),
    Record(Language="B", Parameter="arm", Item="", Cognacy="2"),
    
    Record(Language="C", Parameter="eye", Item="", Cognacy="1"),
    # No ReCord for C 'leg'
    Record(Language="C", Parameter="arm", Item="", Cognacy="3"),

    Record(Language="D", Parameter="eye", Item="", Cognacy="1", loan=True),
    Record(Language="D", Parameter="leg", Item="", Cognacy="1"),
    Record(Language="D", Parameter="leg", Item="", Cognacy="2"),
    Record(Language="D", Parameter="arm", Item="", Cognacy="2,3"),
]

maker = NexusMaker(data)

maker = NexusMakerAscertained(data)  # adds Ascertainment bias character

maker = NexusMakerAscertainedWords(data)  # adds Ascertainment character per word
nex = maker.make()
maker.write(nex, filename="output.nex")


```

### Version History:

* 2.0.4: add `unique_ids` parameter 
* 2.0.3: handle CLDF datasets
* 2.0.2: add tool to filter combining cognates
* 2.0.1: minor bugfixes.
* 2.0: major refactor of testing and other components.
* 1.5: do more validation of cognate sets to detect possibly broken combined cognate sets.
* 1.4: normalise order of cognates (i.e. so 1,54 == 54,1).
* 1.3: handle cognates of form '1a'.
* 1.2: initial release.
