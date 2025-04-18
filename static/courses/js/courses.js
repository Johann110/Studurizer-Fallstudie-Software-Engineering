$('select.dual-listbox-student').bootstrapDualListbox({
nonSelectedListLabel: 'Alle Teilnehmer',
selectedListLabel: 'Zugewiesene Teilnehmer',
preserveSelectionOnMove: 'moved',
moveOnSelect: false,
filterPlaceHolder: 'Suche',
infoText: 'Gesamt: {0}',
infoTextFiltered: '<span class="label label-warning">Gefiltert</span> {0} von {1}',
infoTextEmpty: 'Keine Teilnehmer verfügbar'
});

$('select.dual-listbox-teacher').bootstrapDualListbox({
nonSelectedListLabel: 'Alle Lehrer',
selectedListLabel: 'Zugewiesene Lehrer',
preserveSelectionOnMove: 'moved',
moveOnSelect: false,
filterPlaceHolder: 'Suche',
infoText: 'Gesamt: {0}',
infoTextFiltered: '<span class="label label-warning">Gefiltert</span> {0} von {1}',
infoTextEmpty: 'Keine Lehrer verfügbar'
});