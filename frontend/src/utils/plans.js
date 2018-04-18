import IntervalTree from 'interval-tree2'
import randomColor from 'randomcolor'

/**
 *  Partitions plans based on their collided time intervals.
 *  For example if we have 4 plans like this:
 *    (1)   -------
 *    (2)     -------
 *    (3)       -------------
 *    (4)                       ----
 *
 *  Then plans 1, 2, 3 would be in the same partition and color.
 */
function partitionPlans (plans, midday) {
  if (plans === undefined || plans.length === 0) {
    return []
  }
  // Sort plans based on their start point.
  plans = plans.map((p) => ({
    id: p.id,
    start: p.start.getTime(),
    end: p.end.getTime(),
    desc: p.desc
  })).sort((p1, p2) => p1.start > p2.start)

  let coloredPlans = []

  const itree = new IntervalTree(midday)

  plans.forEach((p) => {
    itree.add(p.start, p.end, p.id)
  })

  /**
   *  Finds next interval with bigger starting point than
   *    the given threshold.
   */
  function nextInterval (intervals, threshold) {
    for (let idx = 0; idx < intervals.length; idx++) {
      if (intervals[idx].start > threshold) {
        return intervals[idx]
      }
    }
    return undefined
  }

  /**
   *  Recursively iterates plan intervals (starting with the least one)
   *    to find maximum sized partitions of time intervals intervening
   *      with each other.
   */
  function maximizeCollisions (interval, set) {
    if (set === undefined) {
      set = new Set()
    }

    const cols = itree.rangeSearch(interval.start, interval.end)

    set = new Set([...set, ...new Set(cols.map((iv) => iv.id))])

    const newEnd = cols.sort((x, y) => y.end > x.end)[0].end
    if (newEnd === interval.end) {
      // Put same color for colliding plans.
      const groupedColor = randomColor({luminosity: 'dark'})
      set.forEach(function (el) {
        coloredPlans.push({
          ...plans.find((p) => p.id === el),
          color: groupedColor
        })
      })

      const nxtIv = nextInterval(plans, newEnd)
      if (nxtIv) {
        return maximizeCollisions(nxtIv, undefined)
      } else {
        return coloredPlans
      }
    } else {
      return maximizeCollisions({start: interval.start, end: newEnd})
    }
  }

  return maximizeCollisions({start: plans[0].start, end: plans[0].end}, undefined)
}

export default partitionPlans
