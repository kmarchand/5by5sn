# 5by5 Show Notes AlfredWorkflow

This workflow retrieves the list of podcasts and show art currently listed at http://5by5.tv/broadcasts and for the selected show, will determine the most recent episode then retrieve show note links for that episode.

## Usage

* `sn` list all shows found, which are filtered as you type 
* `shownotes for {query}` retrieve show notes for the latest episode of a specified show.  The show's short name (what appears in the URL on the show's page after 5by5.tv/...) must be specified.

If you hit `enter` on a selected show name from the `sn` keyword it will automatically launch the `shownotes for {showname}` search to get the recent show notes.

![screenshot1](https://raw.github.com/kmarchand/5by5sn/master/5by5sn-1.png "Screenshot1")
![screenshot2](https://raw.github.com/kmarchand/5by5sn/master/5by5sn-2.png "Screenshot2")

## Note

This workflow was not written in coordination with 5by5 and a change to the layout of the site could cause it to no longer work.


## Changes

* March  9 2014; inital version