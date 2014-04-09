require('iuplua')

-- Text Box --
textBox = iup.multiline {expand='YES'}


----------------------------------------------------------------------

-- Buttons -- 
local textColourBtn = iup.button {title='Text'}
local bgColourBtn = iup.button {title='Background'}

function textColourBtn:action()
  
end

function bgColourBtn:action()

end

btnBox = iup.hbox {textColourBtn, bgColourBtn; gap=4, expand='NO'}
----------------------------------------------------------------------

appBox = iup.vbox {textBox, btnBox; aligment='ACENTER'}

dialog = iup.dialog {appBox; title='Lua Scripting Lab 8', size='HALFxHALF'}

-- Kick off the application
dialog:show()
iup.MainLoop()
