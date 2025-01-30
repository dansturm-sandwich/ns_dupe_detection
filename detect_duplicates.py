import hiero


def detect_duplicates():
  seq = hiero.ui.activeSequence()
  all_shots = []
  tracks = seq.videoTracks()
  for track in tracks:
    shots = list(track.items())
    all_shots.extend(shots)

  clipMatches = {}
  for shot in all_shots:
    clipName = shot.source().name()
    if clipName in clipMatches.keys():
      clipMatches[clipName]+=[{'trackItem':shot,
                               'clip':shot.source(),
                               'duration':shot.duration(),
                               'sourceIn':shot.sourceIn(),
                               'sourceOut':shot.sourceOut()
                               }]
    else:
      clipMatches[clipName]=[{'trackItem':shot,
                               'clip':shot.source(),
                               'duration':shot.duration(),
                               'sourceIn':shot.sourceIn(),
                               'sourceOut':shot.sourceOut()
                               }]


  DFTrack = hiero.core.VideoTrack("Duplicate Frames")
  seq.addTrack(DFTrack)

  hiero.core.clipMatches = clipMatches
  for clipName in clipMatches.keys():
    clip = clipMatches[clipName]
    clip.sort(key=lambda ti: ti["sourceIn"])

    for i, ti in enumerate(clip[:-1]):
      nti = clip[i+1]
      if ti["sourceOut"] >= nti["sourceIn"]:
          DFTrackItem = DFTrack.createTrackItem(ti["trackItem"].name() + " - " + nti["trackItem"].name())
          overlap =  int(ti["sourceOut"] - nti["sourceIn"])
          source = hiero.core.MediaSource().createOfflineVideoMediaSource("offline", 0, overlap+1, seq.framerate(), 0)
          DFTrackItem.setTimelineIn(ti["trackItem"].timelineOut() - overlap)
          DFTrackItem.setSource(source)
          DFTrack.addItem(DFTrackItem)