"""Test script for GUI components.

This script creates a test window to verify all GUI components are working correctly.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

import customtkinter as ctk
from gui.widgets.file_selector import FileSelector
from gui.widgets.provider_selector import ProviderSelector
from gui.widgets.progress_display import ProgressDisplay
from gui.utils import get_theme_manager


class ComponentTestWindow(ctk.CTk):
    """Test window for GUI components."""
    
    def __init__(self):
        super().__init__()
        
        self.title("GUI组件测试 - PPT Translator")
        self.geometry("1000x800")
        
        # Initialize theme
        self.theme_manager = get_theme_manager()
        
        # Create UI
        self._create_widgets()
        
        # Test data
        self.selected_files = []
    
    def _create_widgets(self):
        """Create all widgets."""
        # Main container with tabs
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill='both', expand=True, padx=10, pady=10)
        
        # File Selector Tab
        self.tabview.add("文件选择")
        self.file_selector = FileSelector(
            self.tabview.tab("文件选择"),
            on_selection_changed=self._on_files_selected
        )
        self.file_selector.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Provider Selector Tab
        self.tabview.add("提供商设置")
        self.provider_selector = ProviderSelector(
            self.tabview.tab("提供商设置"),
            on_config_changed=self._on_config_changed
        )
        self.provider_selector.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Progress Display Tab
        self.tabview.add("进度显示")
        self.progress_display = ProgressDisplay(
            self.tabview.tab("进度显示"),
            on_cancel=self._on_progress_cancel
        )
        self.progress_display.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Test Controls
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        ctk.CTkLabel(
            self.control_frame,
            text="测试控制:",
            font=self.theme_manager.get_font('heading_small')
        ).pack(side='left', padx=10, pady=10)
        
        ctk.CTkButton(
            self.control_frame,
            text="模拟进度",
            command=self._simulate_progress
        ).pack(side='left', padx=5, pady=10)
        
        ctk.CTkButton(
            self.control_frame,
            text="添加测试日志",
            command=self._add_test_logs
        ).pack(side='left', padx=5, pady=10)
        
        ctk.CTkButton(
            self.control_frame,
            text="保存配置",
            command=self._save_config
        ).pack(side='left', padx=5, pady=10)
        
        ctk.CTkButton(
            self.control_frame,
            text="退出",
            command=self.destroy,
            fg_color=self.theme_manager.get_color('error')
        ).pack(side='right', padx=10, pady=10)
    
    def _on_files_selected(self, files):
        """Handle file selection."""
        self.selected_files = files
        print(f"Selected {len(files)} files:")
        for f in files:
            print(f"  - {f}")
    
    def _on_config_changed(self, config):
        """Handle config changes."""
        print("Configuration changed:")
        print(f"  Provider: {config.get('provider')}")
        print(f"  Model: {config.get('model')}")
        print(f"  Source: {config.get('source_language')}")
        print(f"  Target: {config.get('target_language')}")
    
    def _on_progress_cancel(self):
        """Handle progress cancel."""
        print("Progress cancelled by user")
        self.progress_display.add_log("用户取消了操作")
    
    def _simulate_progress(self):
        """Simulate a translation progress."""
        import threading
        import time
        
        def run_simulation():
            progress = self.progress_display
            progress.start_progress()
            
            total_files = 3
            for i in range(total_files):
                if not progress.is_running:
                    break
                
                # File processing
                for j in range(10):
                    if not progress.is_running:
                        break
                    
                    percentage = ((i * 10 + j + 1) / (total_files * 10)) * 100
                    progress.update_progress(
                        percentage,
                        f"正在翻译文件 {i + 1}/{total_files}...",
                        i + 1,
                        total_files
                    )
                    time.sleep(0.2)
                
                progress.add_log(f"文件 {i + 1} 处理完成")
            
            if progress.is_running:
                progress.update_progress(100, "翻译完成！", total_files, total_files)
                progress.add_log("所有文件处理完成")
            
            progress.stop_progress()
        
        thread = threading.Thread(target=run_simulation)
        thread.daemon = True
        thread.start()
    
    def _add_test_logs(self):
        """Add test log messages."""
        import random
        
        messages = [
            "正在初始化翻译引擎...",
            "连接至翻译服务...",
            "正在解析PPT文件...",
            "提取文本内容...",
            "正在翻译第1页...",
            "检测到表格内容...",
            "正在处理图片...",
            "保存翻译结果...",
            "正在生成输出文件...",
            "清理临时文件...",
        ]
        
        for _ in range(5):
            msg = random.choice(messages)
            self.progress_display.add_log(msg)
    
    def _save_config(self):
        """Save current configuration."""
        try:
            # Save provider config
            self.provider_selector.save_config()
            
            # Show success message
            import tkinter.messagebox as messagebox
            messagebox.showinfo("成功", "配置已保存！")
            
        except Exception as e:
            import tkinter.messagebox as messagebox
            messagebox.showerror("错误", f"保存配置失败: {e}")


def main():
    """Main entry point."""
    # Set theme
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    
    # Create and run test window
    app = ComponentTestWindow()
    app.mainloop()


if __name__ == '__main__':
    main()
