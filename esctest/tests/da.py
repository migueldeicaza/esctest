import escargs
import esccmd
import escio
from escutil import AssertEQ, knownBug

class DATests(object):
  @knownBug(terminal="iTerm2", reason="iTerm2 doesn't report 18 or 22.")
  def handleDAResponse(self):
    params = escio.ReadCSI('c', expected_prefix='?')
    if escargs.args.expected_terminal == "xterm":
      # This is for a default build. There are various options that could
      # change this, both compile-time and run-time.
      if escargs.args.max_vt_level == 5:
        expected = [65, 1, 2, 6, 9, 15, 18, 21, 22, 29]
      elif escargs.args.max_vt_level == 4:
        expected = [64, 1, 2, 6, 9, 15, 18, 21, 22, 29]
      elif escargs.args.max_vt_level == 3:
        expected = [63, 1, 2, 6, 9, 15, 22, 29]
      elif escargs.args.max_vt_level == 2:
        expected = [62, 1, 2, 6, 9, 15, 22, 29]
      elif escargs.args.max_vt_level == 1:
        expected = [1, 2] # xterm extension (VT100)
      else:
        expected = [0] # xterm extension
    elif escargs.args.expected_terminal == "iTerm2":
      # TODO: Determine which VT levels are completely supported an add 6, 62, 63, or 64.
      # I believe 18 means we support DECSTB and DECSLRM but I can't find any
      # evidence to substantiate this belief.
      expected = [1, 2, 18, 22]
    AssertEQ(params, expected)

  def test_DA_NoParameter(self):
    esccmd.DA()
    self.handleDAResponse()

  def test_DA_0(self):
    esccmd.DA(0)
    self.handleDAResponse()



