# -*- #################
# ---------------------------------------------------------------------------
# GDBCompress.py
# Created on: 2018-10-02 18:30:00
#   (created by ASA/amarcucci)
# Usage: GDBCompress <Tool> <TGN> 
# Description: Administracion de la base de datos
# ---------------------------------------------------------------------------

# Import arcpy module
import os
import io
import datetime
import arcpy
import time
from datetime import date

global text_file

############################################################
# define the log function
def log(message):
    strFile = STARTUP_PATH
    strFile = strFile + file_output
    global text_file
    if text_file == None:
        arcpy.AddMessage("Creating LOG file")
        text_file = open(strFile, "w")
    text_file.write("\n" + str(datetime.datetime.now()) + " " + message)
    
    arcpy.AddMessage(message)

############################################################
# MAIN
text_file = None
STARTUP_PATH = os.path.dirname(__file__)
timestr = time.strftime("%Y%m%d-%H%M%S")
file_output = "\\logs\\file-" + timestr + ".txt"

try:
    log('-' * 40)

    # Set the workspace
    arcpy.env.workspace = STARTUP_PATH + "//admin.sde"

    # Set a variable for the workspace
    adminConn = arcpy.env.workspace

    # Block new connections to the database.
    log("The database is no longer accepting connections")
    arcpy.AcceptConnections(adminConn, False)

    # Wait 2 segundos
    time.sleep(2)

    # Disconnect all users from the database.
    log("Disconnecting all users")
    arcpy.DisconnectUser(adminConn, "ALL")

    # Get a list of versions to pass into the ReconcileVersions tool.
    # Only reconcile versions that are children of Default
    log("Compiling a list of versions to reconcile")
    verList = arcpy.ListVersions(adminConn)
	#verList = [u"DATAOWN.QA1", u"DATAOWN.QA2"]
 
    # Execute the ReconcileVersions tool.
    log("Reconciling all versions")
    arcpy.ReconcileVersions_management(adminConn, "ALL_VERSIONS", "sde.DEFAULT", verList, "LOCK_ACQUIRED", "NO_ABORT", "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", "KEEP_VERSION", STARTUP_PATH + "/logs/reconcilelog_" + timestr  +  ".txt")

    # Run the compress tool.
    log("Running compress")
    arcpy.Compress_management(adminConn)

    # Allow the database to begin accepting connections again
    log("Allow users to connect to the database again")
    arcpy.AcceptConnections(adminConn, True)

    # Update statistics and indexes for the system tables
    # Note: to use the "SYSTEM" option the user must be an geodatabase or database
    # administrator.
    # Rebuild indexes on the system tables
    log("Rebuilding indexes on the system tables")
    arcpy.RebuildIndexes_management(adminConn, "SYSTEM")

    # Obtener listado de todos los feature classes de la GDB
    # Obtener lista de tablas y features standalone. Opcional lista de rasters.
    log("Gather list of standalone tables, feature classes in GDB")
    lista= arcpy.ListTables() + arcpy.ListFeatureClasses() #+ arcpy.ListRasters()
    
    # Obtener lista de tablas y features dentro de Datasets. Opcional lista de rasters.
    # Primero, se obtiene la lista de datasets
    log("Gather list of feature classes and tables contained in datasets")
    datasets = arcpy.ListDatasets("", "Feature")
    
    #Luego por cada dataset, se listan los feature classes y datasets y se agregan a la lista
    for dataset in datasets:
        arcpy.env.workspace = os.path.join(adminConn,dataset)
        datasetFeatureList = arcpy.ListFeatureClasses() + arcpy.ListDatasets()
        lista += datasetFeatureList
    
    #reset del workspace
    arcpy.env.workspace = adminConn
    
    #Update statistics on all feature classes
    log("Updating statistics on all feature classes, tables and System tables")
    arcpy.AnalyzeDatasets_management(
        input_database = arcpy.env.workspace, 
        include_system = "SYSTEM", 
        in_datasets = lista, 
        analyze_base = "ANALYZE_BASE", 
        analyze_delta = "ANALYZE_DELTA", 
        analyze_archive = "ANALYZE_ARCHIVE")
    
    log(" [END] - OK")
except Exception, e:
    log("|Error!!\n   " + str(e) + ']')

    log("Allow users to connect to the database again")
    arcpy.AcceptConnections(adminConn, True)
    raise
