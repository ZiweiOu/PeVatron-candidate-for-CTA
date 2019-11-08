import gammalib
import ctools
import cscripts

# We follow the pipeline of the tutorial in 2017-10-02 in Meudon
# We take RX j1713.7-3946 as an example

"""

# Selecting relevant observations - csobsselect

obsselect = cscripts.csobsselect()
obsselect['inobs'] = '/vol0/1dc/obs/obs_gps_baseline.xml'
obsselect['outobs'] = 'obs_rxj1713.xml'
obsselect['pntselect'] = 'CIRCLE'
obsselect['coordsys'] = 'GAL'
obsselect['glon'] = 347.34
obsselect['glat'] = -0.47
obsselect['rad'] = 3.0
obsselect['tmin'] = 'INDEF'
obsselect['tmax'] = 'INDEF'
obsselect.execute()
#print(obsselect.obs()[0])


# Inspect selected observations - csobsinfo

debug = True

obsinfo = cscripts.csobsinfo()
obsinfo['inobs'] = 'obs_rxj1713.xml'
obsinfo['outds9file'] = 'ds9_rxj1713.reg'
obsinfo.execute()


# Selecting relevant events - ctselect

select = ctools.ctselect()
select['inobs'] = 'obs_rxj1713.xml'
select['outobs'] = 'obs_selected_rxj1713.xml'
select['ra'] = 'UNDEF'
select['dec'] = 'UNDEF'
select['rad'] = 'UNDEF'
select['tmin'] = 'NONE'
select['tmax'] = 'NONE'
select['emin'] = 0.1
select['emax'] = 100
select.execute()



# Generating a sky map from the events - ctskymap

skymap = ctools.ctskymap()
skymap['inobs'] = 'obs_selected_rxj1713.xml'
skymap['outmap'] = 'skymap_rxj1713.fits'
skymap['emin'] = 0.1
skymap['emax'] = 100
skymap['nxpix'] = 200
skymap['nypix'] = 200
skymap['binsz'] = 0.05
skymap['coordsys'] = 'GAL'
skymap['xref'] = 347.34
skymap['yref'] = -0.47
skymap['proj'] = 'CAR'
skymap['bkgsubtract'] = 'NONE'
skymap.execute()

# Finding sources in the sky map - cssrcdetect

srcdet = cscripts.cssrcdetect()
srcdet['inmap'] = 'skymap_rxj1713.fits'
srcdet['srcmodel'] = 'POINT'
srcdet['bkgmodel'] = 'IRF'
srcdet['threshold'] = 5.0
srcdet['outmodel'] = 'models_rxj1713.xml'
srcdet['outds9file'] = 'models_rxj1713.reg'
srcdet['maxsrcs'] = 1
srcdet.execute()



# Stacking the observations - ctbin

bin = ctools.ctbin()
bin['inobs'] = 'obs_selected_rxj1713.xml'
bin['xref'] = 347.34
bin['yref'] = -0.47
bin['proj'] = 'CAR'
bin['coordsys'] = 'GAL'
bin['binsz'] = 0.02
bin['nxpix'] = 200
bin['nypix'] = 200
bin['ebinalg'] = 'LOG'
bin['emin'] = 0.1
bin['emax'] = 100
bin['enumbins'] = 23
bin['outcube'] = 'cntcube_rxj1713.fits'
bin.execute()


# Stacking the observations - ctexpcube

expcube = ctools.ctexpcube()
expcube['inobs'] = 'obs_selected_rxj1713.xml'
expcube['incube'] = 'cntcube_rxj1713.fits'
expcube['outcube'] = 'expcube_rxj1713.fits'
expcube.execute()

# Stacking the observations - ctpsfcube

psfcube = ctools.ctpsfcube()
psfcube['inobs'] = 'obs_selected_rxj1713.xml'
psfcube['incube'] = 'NONE'
psfcube['outcube'] = 'psfcube_rxj1713.fits'
psfcube['emin'] = 0.1
psfcube['emax'] = 100
psfcube['enumbins'] = 23
psfcube['nxpix'] = 10
psfcube['nypix'] = 10
psfcube['ebinalg'] = 'LOG'
psfcube['binsz'] = 1.0
psfcube['coordsys'] = 'GAL'
psfcube['proj'] = 'CAR'
psfcube['xref'] = 347.34
psfcube['yref'] = -0.47
psfcube.execute()

# ctedispcube

edispcube = ctools.ctedispcube()
edispcube['inobs'] = 'obs_selected_rxj1713.xml'
edispcube['incube'] = 'NONE'
edispcube['outcube'] = 'edispcube_rxj1713.fits'
edispcube['emin'] = 0.1
edispcube['emax'] = 100
edispcube['enumbins'] = 23
edispcube['xref'] = 347.34
edispcube['yref'] = -0.47
edispcube['ebinalg'] = 'LOG'
edispcube['coordsys'] = 'GAL'
edispcube['proj'] = 'CAR'
edispcube['binsz'] = 1.0
edispcube['nxpix'] = 10
edispcube['nypix'] = 10
edispcube.execute()



# Stacking the observations - ctbkgcube

bkgcube = ctools.ctbkgcube()
bkgcube['inobs'] = 'obs_selected_rxj1713.xml'
bkgcube['inmodel'] = 'models_rxj1713_new_IEM.xml'
bkgcube['incube'] = 'cntcube_rxj1713.fits'
bkgcube['outcube'] = 'bkgcube_rxj1713_new_IEM.fits'
bkgcube['outmodel'] = 'models_cube_rxj1713_new_IEM.xml'
bkgcube.execute()



# Maximum likelihood fitting - ctlike

debug = True
edisp = True

like = ctools.ctlike()
like['inobs'] = 'cntcube_rxj1713.fits'
like['inmodel'] = 'models_cube_rxj1713_new_IEM.xml'
like['expcube'] = 'expcube_rxj1713.fits'
like['psfcube'] = 'psfcube_rxj1713.fits'
like['bkgcube'] = 'bkgcube_rxj1713_new_IEM.fits'
like['outmodel'] = 'results_rxj1713_new_IEM.xml'
like.execute()



# Generating a butterfly diagram - ctbutterfly

edisp = True

butterfly = ctools.ctbutterfly()
butterfly['inobs'] = 'cntcube_rxj1713.fits'
butterfly['inmodel'] = 'results_rxj1713.xml'
butterfly['srcname'] = 'Src001'
butterfly['expcube'] = 'expcube_rxj1713.fits'
butterfly['psfcube'] = 'psfcube_rxj1713.fits'
butterfly['edispcube'] = 'edispcube_rxj1713.fits'
butterfly['bkgcube'] = 'bkgcube_rxj1713.fits'
butterfly['outfile'] = 'butterfly_rxj1713.txt'
butterfly['emin'] = 0.1
butterfly['emax'] = 100
butterfly.execute()



# Inspecting the residuals - csresmap

edisp = True

resmap = cscripts.csresmap()
resmap['inobs'] = 'cntcube_rxj1713.fits'
resmap['modcube'] = 'NONE'
resmap['expcube'] = 'expcube_rxj1713.fits'
resmap['psfcube'] = 'psfcube_rxj1713.fits'
resmap['edispcube'] = 'edispcube_rxj1713.fits'
resmap['bkgcube'] = 'bkgcube_rxj1713_new_IEM.fits'
resmap['inmodel'] = 'results_rxj1713_new_IEM.xml'
resmap['algorithm'] = 'SIGNIFICANCE'
resmap['outmap'] = 'resmaps_rxj1713_new_IEM.fits'
resmap.execute()



# Generating a residual spectrum - csresspec

component = True
edisp = True
mask = False

resspec = cscripts.csresspec()
resspec['inobs'] = 'cntcube_rxj1713.fits'
resspec['modcube'] = 'NONE'
resspec['expcube'] = 'expcube_rxj1713.fits'
resspec['psfcube'] = 'psfcube_rxj1713.fits'
resspec['edispcube'] = 'edispcube_rxj1713.fits'
resspec['bkgcube'] = 'bkgcube_rxj1713_new_IEM.fits'
resspec['emin'] = 0.1
resspec['emax'] = 100
resspec['enumbins'] = 23
resspec['coordsys'] = 'GAL'
resspec['proj'] = 'CAR'
resspec['xref'] = 347.34
resspec['yref'] = -0.47
resspec['nxpix'] = 10
resspec['nypix'] = 10
resspec['binsz'] = 1.0
resspec['inmodel'] = 'results_rxj1713_new_IEM.xml'
resspec['algorithm'] = 'SIGNIFICANCE'
resspec['outfile'] = 'resspec_rxj1713_new_IEM.fits'
resspec.execute()

"""

# Generating a SED - csspec 

edisp = True

spec = cscripts.csspec()
spec['inobs'] = 'cntcube_rxj1713.fits'
spec['expcube'] = 'expcube_rxj1713.fits'
spec['psfcube'] = 'psfcube_rxj1713.fits'
spec['edispcube'] = 'edispcube_rxj1713.fits'
spec['bkgcube'] = 'bkgcube_rxj1713_new_IEM.fits'
spec['inmodel'] = 'results_rxj1713_new_IEM.xml'
spec['srcname'] = 'Src001'
spec['ebinalg'] = 'LOG'
spec['method'] = 'AUTO'
spec['emin'] = 0.1
spec['emax'] = 100
spec['enumbins'] = 23
spec['outfile'] = 'spectrum_rxj1713_new_IEM.fits'
spec.execute()


