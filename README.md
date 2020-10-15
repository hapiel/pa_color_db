# Pixel Art search tool

## MongoDB queries

Get all images containing the color red:
```
  { colors: { $elemMatch: { "$and": [ {"rgb.0": 255}, {"rgb.1": 0}, {"rgb.2": 0} ] } } }
```

