/*
Copyright (c) 2003-2009, CKSource - Frederico Knabben. All rights reserved.
For licensing, see LICENSE.html or http://ckeditor.com/license
*/

CKEDITOR.editorConfig = function( config )
{
	config.enterMode = CKEDITOR.ENTER_BR;
	config.templates = 'twitter,default';
	config.templates_files = [
	                          	'/media/js/ckeditor_templates.js',
	                          	'/media/js/plugins/templates/templates/default.js'
	                          ];
	
	config.toolbar = 'WidgetToolbar';
	
	config.toolbar_WidgetToolbar = 
		[
		    ['Templates','-','Source','-','Save','NewPage','Preview','-'],
		    ['Cut','Copy','Paste','PasteText','PasteFromWord','-'],
		    ['Undo','Redo','-','Find','Replace','-','SelectAll','RemoveFormat'],
		    '/',
		    ['Bold','Italic','Underline','Strike','-','Subscript','Superscript'],
		    ['NumberedList','BulletedList','-','Outdent','Indent','Blockquote'],
		    ['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],
		    ['Link','Unlink','Anchor'],
		    ['Image','Flash','Table','HorizontalRule','Smiley','SpecialChar','PageBreak'],
		    '/',
		    ['Styles','Format','Font','FontSize'],
		    ['TextColor','BGColor'],
		    ['Maximize', 'ShowBlocks','-','About']
		];
};
