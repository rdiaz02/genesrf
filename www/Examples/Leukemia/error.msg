Loading required package: randomForest
Read 1 item
Read 1 item
Read 1 item
Read 0 items
Read 39 items
Warning in varSelRF(xdata, Class, fitted.rf = rf1) : 
	 Using as ntree and mtry the parameters obtained from fitted.rf
Warning in varSelRFBoot(xdata, Class, srf = rf.vs1, TheCluster = TheCluster,  : 
	 Using as ntree and mtryFactor the parameters obtained from srf
Warning message:
the condition has length > 1 and only the first element will be used in: if (class(trycode) == "try-error") caughtOurError(paste("Could not run randomVarImpsRF, with error",  
Error in mpi.comm.disconnect(comm) : It seems no members(slaves) associated with comm 1
-----------------------------------------------------------------------------
It seems that there is no lamd running on the host karl02.

This indicates that the LAM/MPI runtime environment is not operating.
The LAM/MPI runtime environment is necessary for the "lamhalt" command.

Please run the "lamboot" command the start the LAM/MPI runtime
environment.  See the LAM/MPI documentation for how to invoke
"lamboot" across multiple machines.
-----------------------------------------------------------------------------
