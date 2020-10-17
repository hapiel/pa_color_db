# Pixel Art search tool

## MongoDB queries

Get all images containing the color red:
```
  { colors: { $elemMatch: { "$and": [ {"rgb.0": 255}, {"rgb.1": 0}, {"rgb.2": 0} ] } } }
```

Get all image within red range:

```
{ colors: { $elemMatch: { "$and": [ {"rgb.0": {$gte: 250, $lte: 255}}, {"rgb.1": 10}, {"rgb.2": 10} ] } } }
```

