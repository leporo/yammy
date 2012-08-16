--------------------------------------------------------------------------------

Instructions for adding Yammy template syntax highlighting / coloring to the
Colorer-take5 Eclipse plug-in.

--------------------------------------------------------------------------------

Requirements:

 - Eclipse IDE. Get it here:
      
        http://www.eclipse.org/

 - Colorer-take5 plug-in for Eclipse IDE - use only version 0.8.0 (or later).
   Get it here:
        
        http://sourceforge.net/projects/colorer/files/Eclipse%20Colorer/

--------------------------------------------------------------------------------

Step by step plug-in set-up:

-----

1. Install Eclipse if it is not already installed.

-----

2. Install Colorer-take5 plug-in (manual installation only):

http://colorer.sf.net/eclipsecolorer/

-----

3. Install the *.hrc files:

Locate the 'common.jar' file in:

~/.eclipse/org.eclipse.platform_3.x.x_xxxxxxx/plugins/net.sf.colorer_0.x.x/colorer/hrc/

Open the 'common.jar' file in an archive manager of your choice (just open it
rather than unpacking it), and navigate to the 'rare' folder.

Copy the yammy.hrc file to the 'rare' folder.

-----

4. Edit existing files to let the Colorer-take5 plug-in know about the files we
added to it.

Navigate to:

~/.eclipse/org.eclipse.platform_3.x.x_xxxxxxx/plugins/net.sf.colorer_0.x.x/colorer/hrc/

and open the 'proto.hrc' file located in the 'hrc' sub-directory. This file
contains all the language prototypes for which the Colorer plug-in can provide
syntax coloring. 

Search for this text within the file:

<prototype name="avr"

The search should get you to the last entry in the 'rare languages' section of
the file. The entire entry should look like this (excluding the dashed lines
added here to offset the code):

-----------------------------------------------------------
  <prototype name="avr" group="rare" description="AVR asm">
    <location link="jar:common.jar!rare/avr-5.hrc"/>
    <filename>/\.(asm|inc|avr)$/i</filename>
    <firstline>/^\s*;/</firstline>
  </prototype>
-----------------------------------------------------------

Now, copy the following (again, excluding the dashed lines) and paste it just
below the entry you found with your search (the 'My Rare' comment is not
required, of course):

-----------------------------------------------------------
  <prototype name="yammy" group="rare" description="Yammy Template">
        <location link="jar:common.jar!rare/yammy.hrc"/>
        <filename>/\.(ymy)$/i</filename>
  </prototype>
-----------------------------------------------------------

-----

5. Start (or restart) Eclipse.

-----

6. Test it out:

Open a *.ymy or *.yammy file and see how it works.

-----

Notes: 

- Useful links to Colorer-take5 HRC and HRD documentation:
  
  HRC Language Reference
  http://colorer.sourceforge.net/hrc-ref/

  HRD Spec
  http://colorer.sourceforge.net/hrc-ref/#ref.hrd.hrd
