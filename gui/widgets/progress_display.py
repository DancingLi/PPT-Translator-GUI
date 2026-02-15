"""Progress display component for PPT Translator GUI.

Provides a reusable component for displaying translation progress with
progress bars, status messages, and real-time logs.
"""

import time
from typing import Optional, Callable
from datetime import datetime, timedelta
import customtkinter as ctk

from ..utils.theme_manager import get_theme_manager


class ProgressDisplay(ctk.CTkFrame):
    """Progress display component for showing translation progress.
    
    Displays overall progress bar, current operation status, file counters,
    estimated time remaining, and a scrollable log area.
    
    Attributes:
        is_running: Whether translation is currently running
        on_cancel: Callback function when cancel button is clicked
    
    Example:
        >>> progress = ProgressDisplay(parent)
        >>> progress.pack(fill='both', expand=True)
        >>> progress.start_progress()
        >>> progress.update_progress(50, "Processing...")
        >>> progress.add_log("Processing file 1 of 5")
    """
    
    def __init__(
        self,
        master,
        on_cancel: Optional[Callable[[], None]] = None,
        **kwargs
    ):
        """Initialize progress display component.
        
        Args:
            master: Parent widget
            on_cancel: Callback function when cancel button is clicked
            **kwargs: Additional arguments passed to CTkFrame
        """
        super().__init__(master, **kwargs)
        
        self.theme_manager = get_theme_manager()
        self.on_cancel = on_cancel
        self.is_running = False
        self.start_time: Optional[datetime] = None
        
        self._create_widgets()
        self._apply_theme()
    
    def _create_widgets(self) -> None:
        """Create and layout all widgets."""
        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="进度",
            font=self.theme_manager.get_font('heading_small')
        )
        self.title_label.pack(anchor='w', padx=10, pady=(10, 5))
        
        # Progress bar frame
        self.progress_frame = ctk.CTkFrame(self)
        self.progress_frame.pack(fill='x', padx=10, pady=5)
        
        # Progress percentage
        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="0%",
            font=self.theme_manager.get_font('heading_small'),
            width=50
        )
        self.progress_label.pack(side='left', padx=10, pady=10)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            height=20
        )
        self.progress_bar.set(0)
        self.progress_bar.pack(side='left', fill='x', expand=True, padx=10, pady=10)
        
        # Status info frame
        self.status_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.status_frame.pack(fill='x', padx=10, pady=5)
        
        # Status message
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="准备就绪",
            font=self.theme_manager.get_font('body_medium')
        )
        self.status_label.pack(side='left')
        
        # File counter
        self.counter_label = ctk.CTkLabel(
            self.status_frame,
            text="",
            font=self.theme_manager.get_font('body_medium')
        )
        self.counter_label.pack(side='right')
        
        # Time estimate
        self.time_label = ctk.CTkLabel(
            self,
            text="",
            font=self.theme_manager.get_font('body_small'),
            text_color=self.theme_manager.get_color('text_secondary')
        )
        self.time_label.pack(anchor='w', padx=10)
        
        # Log area
        self.log_frame = ctk.CTkFrame(self)
        self.log_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.log_label = ctk.CTkLabel(
            self.log_frame,
            text="日志",
            font=self.theme_manager.get_font('body_medium')
        )
        self.log_label.pack(anchor='w', padx=10, pady=(5, 0))
        
        # Log text area with scrollbar
        self.log_text = ctk.CTkTextbox(
            self.log_frame,
            font=self.theme_manager.get_font('monospace'),
            wrap='word',
            height=100
        )
        self.log_text.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Cancel button
        self.cancel_btn = ctk.CTkButton(
            self,
            text="取消",
            command=self._on_cancel_clicked,
            fg_color=self.theme_manager.get_color('error'),
            hover_color=self.theme_manager.get_color('error'),
            state='disabled'
        )
        self.cancel_btn.pack(anchor='e', padx=10, pady=(0, 10))
    
    def _apply_theme(self) -> None:
        """Apply current theme colors to widgets."""
        colors = self.theme_manager.colors
        
        self.configure(fg_color=colors['bg_secondary'])
        self.progress_frame.configure(fg_color=colors['bg_tertiary'])
        self.log_frame.configure(fg_color=colors['bg_tertiary'])
        
        self.log_text.configure(
            fg_color=colors['bg_primary'],
            text_color=colors['text_primary'],
            border_color=colors['border']
        )
        
        self.status_label.configure(text_color=colors['text_primary'])
        self.counter_label.configure(text_color=colors['text_secondary'])
        self.time_label.configure(text_color=colors['text_secondary'])
        self.progress_label.configure(text_color=colors['accent_primary'])
    
    def _on_cancel_clicked(self) -> None:
        """Handle cancel button click."""
        if self.on_cancel:
            self.on_cancel()
    
    def start_progress(self) -> None:
        """Start a new progress session."""
        self.is_running = True
        self.start_time = datetime.now()
        self.log_text.delete('1.0', 'end')
        self.cancel_btn.configure(state='normal')
        self.add_log("开始翻译任务...")
    
    def stop_progress(self) -> None:
        """Stop the current progress session."""
        self.is_running = False
        self.start_time = None
        self.cancel_btn.configure(state='disabled')
        self.add_log("翻译任务已结束")
    
    def update_progress(
        self,
        percentage: float,
        status: str,
        current_file: int = 0,
        total_files: int = 0
    ) -> None:
        """Update progress display.
        
        Args:
            percentage: Progress percentage (0-100)
            status: Current status message
            current_file: Current file number
            total_files: Total number of files
        """
        # Update progress bar
        self.progress_bar.set(percentage / 100)
        self.progress_label.configure(text=f"{int(percentage)}%")
        
        # Update status
        self.status_label.configure(text=status)
        
        # Update counter
        if total_files > 0:
            self.counter_label.configure(text=f"第 {current_file}/{total_files} 个文件")
        
        # Update time estimate
        if self.start_time and self.is_running:
            elapsed = datetime.now() - self.start_time
            if percentage > 0:
                total_estimate = elapsed / (percentage / 100)
                remaining = total_estimate - elapsed
                self.time_label.configure(
                    text=f"已用时间: {self._format_duration(elapsed)} | "
                         f"预计剩余: {self._format_duration(remaining)}"
                )
    
    def add_log(self, message: str) -> None:
        """Add a log message.
        
        Args:
            message: Log message to add
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert('end', log_entry)
        self.log_text.see('end')
    
    def clear_log(self) -> None:
        """Clear all log messages."""
        self.log_text.delete('1.0', 'end')
    
    def _format_duration(self, duration) -> str:
        """Format duration as human readable string.
        
        Args:
            duration: timedelta object or seconds
            
        Returns:
            Formatted duration string
        """
        if isinstance(duration, timedelta):
            total_seconds = int(duration.total_seconds())
        else:
            total_seconds = int(duration)
        
        if total_seconds < 60:
            return f"{total_seconds}秒"
        elif total_seconds < 3600:
            minutes = total_seconds // 60
            seconds = total_seconds % 60
            return f"{minutes}分{seconds}秒"
        else:
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{hours}时{minutes}分"


def main():
    """Test the progress display component."""
    import time
    import threading
    
    app = ctk.CTk()
    app.title("Progress Display Test")
    app.geometry("800x600")
    
    progress = ProgressDisplay(app)
    progress.pack(fill='both', expand=True, padx=20, pady=20)
    
    def simulate_progress():
        """Simulate a translation task."""
        progress.start_progress()
        
        total_files = 5
        for i in range(total_files):
            if not progress.is_running:
                break
            
            # Update progress
            percentage = (i / total_files) * 100
            progress.update_progress(
                percentage,
                f"正在翻译文件 {i + 1}/{total_files}...",
                i + 1,
                total_files
            )
            progress.add_log(f"开始处理文件 {i + 1}")
            
            # Simulate work
            for j in range(10):
                if not progress.is_running:
                    break
                time.sleep(0.3)
                sub_progress = percentage + ((j + 1) / 10) * (100 / total_files)
                progress.update_progress(
                    sub_progress,
                    f"正在翻译文件 {i + 1}/{total_files}... ({(j + 1) * 10}%)",
                    i + 1,
                    total_files
                )
            
            progress.add_log(f"文件 {i + 1} 处理完成")
        
        if progress.is_running:
            progress.update_progress(100, "翻译完成！", total_files, total_files)
            progress.add_log("所有文件处理完成")
        
        progress.stop_progress()
    
    def start_test():
        """Start the test simulation."""
        thread = threading.Thread(target=simulate_progress)
        thread.daemon = True
        thread.start()
    
    # Add start button
    start_btn = ctk.CTkButton(app, text="Start Test", command=start_test)
    start_btn.pack(pady=10)
    
    # Set up cancel callback
    def on_cancel():
        progress.is_running = False
        progress.add_log("用户取消了操作")
    
    progress.on_cancel = on_cancel
    
    app.mainloop()


if __name__ == '__main__':
    main()
