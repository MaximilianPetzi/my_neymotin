#include <stdio.h>
#include "hocdec.h"
extern int nrnmpi_myid;
extern int nrn_nobanner_;

extern void _MyExp2SynBB_reg(void);

void modl_reg(){
  if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
    fprintf(stderr, "Additional mechanisms from files\n");

    fprintf(stderr," \"MyExp2SynBB.mod\"");
    fprintf(stderr, "\n");
  }
  _MyExp2SynBB_reg();
}
