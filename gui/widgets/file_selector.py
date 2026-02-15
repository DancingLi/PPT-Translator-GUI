"""File selector component for PPT Translator GUI.

Provides a reusable component for selecting PPT files and folders with
support for single file, multiple files, and folder selection modes.
"""

from typing import List, Callable, Optional
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk

from ..utils.theme_manager import get_theme_manager


class FileSelector(ctk.CTkFrame):
    """File selector component for selecting PPT files and folders.
    
    Provides buttons for selecting single files, multiple files, or folders,
    displays selected items in a scrollable list, and allows removing items.
    
    Attributes:
        selected_files: List of currently selected file paths
        on_selection_changed: Callback function when selection changes
    
    Example:
        >>> selector = FileSelector(parent)
        >>> selector.pack(fill='both', expand=True)
        >>> selector.set_callback(on_files_selected)
    """
    
    def __init__(
        self,
        master,
        on_selection_changed: Optional[Callable[[List[str]], None]] = None,
        file_types: Optional[List[tuple]] = None,
        **kwargs
    ):
        """Initialize file selector component.
        
        Args:
            master: Parent widget
            on_selection_changed: Callback function called when selection changes
            file_types: List of file type tuples for file dialog
                       e.g., [("PowerPoint files", "*.pptx"), ("All files", "*.*")]
            **kwargs: Additional arguments passed to CTkFrame
        """
        super().__init__(master, **kwargs)
        
        self.theme_manager = get_theme_manager()
        self.selected_files: List[str] = []
        self.on_selection_changed = on_selection_changed
        self.file_types = file_types or [("PowerPoint files", "*.pptx"), ("All files", "*.*")]
        
        self._create_widgets()
        self._apply_theme()
    
    def _create_widgets(self) -> None:
        """Create and layout all widgets."""
        # Title label
        self.title_label = ctk.CTkLabel(
            self,
            text="选择文件",
            font=self.theme_manager.get_font('heading_small')
        )
        self.title_label.pack(anchor='w', padx=10, pady=(10, 5))
        
        # Button frame
        self.button_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.button_frame.pack(fill='x', padx=10, pady=5)
        
        # File buttons
        self.select_file_btn = ctk.CTkButton(
            self.button_frame,
            text="选择文件",
            command=self._select_file,
            width=100,
            height=32
        )
        self.select_file_btn.pack(side='left', padx=(0, 5))
        
        self.select_files_btn = ctk.CTkButton(
            self.button_frame,
            text="选择多个文件",
            command=self._select_multiple_files,
            width=100,
            height=32
        )
        self.select_files_btn.pack(side='left', padx=5)
        
        self.select_folder_btn = ctk.CTkButton(
            self.button_frame,
            text="选择文件夹",
            command=self._select_folder,
            width=100,
            height=32
        )
        self.select_folder_btn.pack(side='left', padx=5)
        
        # Clear button
        self.clear_btn = ctk.CTkButton(
            self.button_frame,
            text="清空全部",
            command=self.clear_selection,
            width=80,
            height=32,
            fg_color=self.theme_manager.get_color('error'),
            hover_color=self.theme_manager.get_color('error')
        )
        self.clear_btn.pack(side='right', padx=5)
        
        # File list frame with scrollbar
        self.list_frame = ctk.CTkFrame(self)
        self.list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Scrollable frame for file list
        self.scroll_frame = ctk.CTkScrollableFrame(
            self.list_frame,
            label_text="已选择的文件",
            label_font=self.theme_manager.get_font('body_medium')
        )
        self.scroll_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Empty label
        self.empty_label = ctk.CTkLabel(
            self.scroll_frame,
            text="还没有选择任何文件\n点击上方按钮选择 PPT 文件或文件夹",
            font=self.theme_manager.get_font('body_medium')
        )
        self.empty_label.pack(pady=20)
        
        # Counter label
        self.counter_label = ctk.CTkLabel(
            self,
            text="已选择: 0 个文件",
            font=self.theme_manager.get_font('body_small')
        )
        self.counter_label.pack(anchor='w', padx=10, pady=(0, 10))
    
    def _apply_theme(self) -> None:
        """Apply current theme colors to widgets."""
        colors = self.theme_manager.colors
        
        self.configure(fg_color=colors['bg_secondary'])
        self.list_frame.configure(fg_color=colors['bg_tertiary'])
        self.scroll_frame.configure(
            fg_color=colors['bg_secondary'],
            label_text_color=colors['text_primary']
        )
        self.empty_label.configure(text_color=colors['text_secondary'])
        self.counter_label.configure(text_color=colors['text_secondary'])
    
    def _select_file(self) -> None:
        """Handle single file selection."""
        file_path = filedialog.askopenfilename(
            title="选择 PPT 文件",
            filetypes=self.file_types
        )
        
        if file_path:
            self.add_file(file_path)
    
    def _select_multiple_files(self) -> None:
        """Handle multiple file selection."""
        file_paths = filedialog.askopenfilenames(
            title="选择多个 PPT 文件",
            filetypes=self.file_types
        )
        
        for file_path in file_paths:
            self.add_file(file_path)
    
    def _select_folder(self) -> None:
        """Handle folder selection."""
        folder_path = filedialog.askdirectory(
            title="选择包含 PPT 文件的文件夹"
        )
        
        if folder_path:
            # Find all .pptx files in the folder
            folder = Path(folder_path)
            pptx_files = list(folder.glob('**/*.pptx'))
            
            for file_path in pptx_files:
                self.add_file(str(file_path))
    
    def add_file(self, file_path: str) -> None:
        """Add a file to the selection.
        
        Args:
            file_path: Path to the file to add
        """
        # Normalize path
        file_path = str(Path(file_path).resolve())
        
        # Check if already exists
        if file_path in self.selected_files:
            return
        
        # Add to list
        self.selected_files.append(file_path)
        
        # Update UI
        self._update_file_list()
        
        # Notify callback
        if self.on_selection_changed:
            self.on_selection_changed(self.selected_files.copy())
    
    def remove_file(self, file_path: str) -> None:
        """Remove a file from the selection.
        
        Args:
            file_path: Path to the file to remove
        """
        if file_path in self.selected_files:
            self.selected_files.remove(file_path)
            self._update_file_list()
            
            # Notify callback
            if self.on_selection_changed:
                self.on_selection_changed(self.selected_files.copy())
    
    def clear_selection(self) -> None:
        """Clear all selected files."""
        self.selected_files.clear()
        self._update_file_list()
        
        # Notify callback
        if self.on_selection_changed:
            self.on_selection_changed([])
    
    def get_selected_files(self) -> list:
        """Get list of selected files.
        
        Returns:
            List of selected file paths
        """
        return self.selected_files.copy()
    
    def set_callback(self, callback: Callable[[List[str]], None]) -> None:
        """Set the selection changed callback.
        
        Args:
            callback: Function to call when selection changes
        """
        self.on_selection_changed = callback
    
    def _update_file_list(self) -> None:
        """Update the file list display."""
        # Clear existing widgets
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        
        if not self.selected_files:
            # Show empty label
            self.empty_label = ctk.CTkLabel(
                self.scroll_frame,
                text="还没有选择任何文件\n点击上方按钮选择 PPT 文件或文件夹",
                font=self.theme_manager.get_font('body_medium')
            )
            self.empty_label.pack(pady=20)
        else:
            # Show file list
            for i, file_path in enumerate(self.selected_files):
                self._create_file_item(i, file_path)
        
        # Update counter
        self.counter_label.configure(
            text=f"已选择: {len(self.selected_files)} 个文件"
        )
    
    def _create_file_item(self, index: int, file_path: str) -> None:
        """Create a file item in the list.
        
        Args:
            index: Index of the file in the list
            file_path: Path to the file
        """
        colors = self.theme_manager.colors
        
        # Frame for this item
        item_frame = ctk.CTkFrame(
            self.scroll_frame,
            fg_color=colors['bg_secondary'] if index % 2 == 0 else colors['bg_tertiary'],
            corner_radius=4
        )
        item_frame.pack(fill='x', padx=5, pady=2)
        
        # File name label
        file_name = Path(file_path).name
        name_label = ctk.CTkLabel(
            item_frame,
            text=file_name,
            font=self.theme_manager.get_font('body_medium'),
            anchor='w'
        )
        name_label.pack(side='left', fill='x', expand=True, padx=10, pady=5)
        
        # Remove button
        remove_btn = ctk.CTkButton(
            item_frame,
            text='✕',
            width=28,
            height=28,
            fg_color=colors['error'],
            hover_color=colors['error'],
            command=lambda path=file_path: self.remove_file(path)
        )
        remove_btn.pack(side='right', padx=5, pady=5)