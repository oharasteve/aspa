def getHighRunTarget(handicap):
  if handicap < 100 or handicap >= 850:
    return 0

  # This is a lookup table for calculating high run target,
  # given a player's handicap. It is a piecewise linear function,
  # interpolating between the points
  highRuns = [
    [400, 18],
    [450, 20],
    [500, 22],
    [550, 26],
    [600, 32],
    [650, 44],
    [700, 58],
    [725, 72],
    [750, 86],
    [775, 100],
    [800, 114],
    [825, 128],
    [850, 144]
  ]

  for i in range(len(highRuns)):
    if (handicap < highRuns[i][0]):
        break

  prev_handicap = 0
  prev_target = 0
  if i > 0:
      prev_handicap = highRuns[i-1][0]
      prev_target = highRuns[i-1][1]
  scale = (float(highRuns[i][0]) - prev_handicap) / (highRuns[i][1] - prev_target)
  return round(prev_target + (handicap - prev_handicap) / scale)