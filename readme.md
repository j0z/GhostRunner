Ghost Runner - readme
=====================

Current Version: 06.27.2012
---------------------------
Changed
-------
* Made some experimental changes to items blitting off-screen
* Redraw background on level reset

Previous Version: 06.25.2012
---------------------------
Changed
-------
* Backgrounds
* Some rendering changes
* Somber: draw_sprite_in_background()

Previous Version: 06.20.2012
---------------------------
Changed
-------
* Camera now follows the character correctly
* Platforming fixed
* Somber: Added hfriction_move and hfriction_stop
* Somber: Fixed alpha transparency for PNGs
* Can no longer jump while in the editor

Previous Version: 06.19.2012
---------------------------
Changed
-------
* Added level_pos variable to track the location of the mouse in game coordinates
* Scrolling will cost you $20
* -editor flag
* Somber: set_background_image()
* Somber: set_background_color()
* Crashfix

Previous Version: 06.17.2012
---------------------------
Changed
-------
* Added on_ground flag to character
* Rewrote collision logic
* Added level.py
* Added ghost_object class for use with designer
* Somber: Added mouse events
* Somber: Added `color` argument to somber.write()
* Somber: set_pos() now has a `set_start` flag for setting start_pos
* Somber: get_all_resources()
* Somber: Fixed set_alpha()
* mouse_down()
* load()
* save()
* enter_designer()
* reset_level()
* File format for levels established
* Tile selector in designer

Previous Version: 06.16.2012
---------------------------
Changed
-------
* Fixed sprite drawing off-center
* somber.bind_key(key,function) - Binds a key to a callback function
* somber.add_sprite(file) - Internal use only (used by somber.get_sprite())
* somber.get_sprite(file) - Searches sprite cache for image, returns surface if found (else: creates and caches)
* somber.set_background(file) - Draws 'file' to background surface and blits to screen
* Added automatic sprite caching
* Collisions