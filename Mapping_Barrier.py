import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk
from barrier_determain import extract_pixels      # 提取像素
from raster_to_vector import polygonize_image      # 转写geojson


# 第一页

def browse_input_extraction():
    file_path = filedialog.askopenfilename(
        title="input PNG file",
        filetypes=[("PNG files", "*.png")]
    )
    if file_path:
        extraction_input_entry.delete(0, tk.END)
        extraction_input_entry.insert(0, file_path)

def browse_output_extraction():
    file_path = filedialog.asksaveasfilename(
        title="output PNG file",
        defaultextension=".png",
        filetypes=[("PNG files", "*.png")]
    )
    if file_path:
        extraction_output_entry.delete(0, tk.END)
        extraction_output_entry.insert(0, file_path)

def run_extraction():
    input_path = extraction_input_entry.get().strip()
    output_path = extraction_output_entry.get().strip()
    ranges_text = extraction_ranges_textbox.get("1.0", tk.END).strip()

    if not input_path or not output_path or not ranges_text:
        messagebox.showerror("Error", "missing information")
        return

    rgb_ranges = []
    lines = ranges_text.splitlines()
    for line in lines:
        parts = line.split(',')
        if len(parts) != 6:
            messagebox.showerror("Error", f"Format error: {line}\nExpect: r_min, g_min, b_min, r_max, g_max, b_max")
            return
        try:
            nums = [int(part.strip()) for part in parts]
        except ValueError:
            messagebox.showerror("Error", f"Expect integer in: {line}")
            return
        rgb_min = tuple(nums[0:3])
        rgb_max = tuple(nums[3:6])
        rgb_ranges.append((rgb_min, rgb_max))

    try:
        extract_pixels(input_path, output_path, rgb_ranges)
        messagebox.showinfo("Succeed", f"The file is saved at:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Compile error", f"{e}")


# 第二页

def browse_input_polygon():
    file_path = filedialog.askopenfilename(
        title="Input PNG file",
        filetypes=[("PNG files", "*.png")]
    )
    if file_path:
        polygon_input_entry.delete(0, tk.END)
        polygon_input_entry.insert(0, file_path)

def browse_output_polygon():
    file_path = filedialog.asksaveasfilename(
        title="Output GeoJSON file",
        defaultextension=".geojson",
        filetypes=[("GeoJSON files", "*.geojson")]
    )
    if file_path:
        polygon_output_entry.delete(0, tk.END)
        polygon_output_entry.insert(0, file_path)

def run_polygonization():
    input_path = polygon_input_entry.get().strip()
    output_path = polygon_output_entry.get().strip()
    if not input_path or not output_path:
        messagebox.showerror("Error", "Missing information")
        return
    try:
        polygonize_image(input_path, output_path)
        messagebox.showinfo("Succeed", f"GeoJSON file saved at:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Error during polygonization:\n{e}")


# 主窗口

root = tk.Tk()
root.title("Mapping Barrier")
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# 创建两个标签页
extraction_tab = tk.Frame(notebook)
polygonization_tab = tk.Frame(notebook)
notebook.add(extraction_tab, text="Extract Pixels")
notebook.add(polygonization_tab, text="Polygonize Image")


# 构建第一页

# 输入文件
tk.Label(extraction_tab, text="input image:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
extraction_input_entry = tk.Entry(extraction_tab, width=50)
extraction_input_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(extraction_tab, text="Browse", command=browse_input_extraction).grid(row=0, column=2, padx=5, pady=5)

# 输出文件
tk.Label(extraction_tab, text="output image:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
extraction_output_entry = tk.Entry(extraction_tab, width=50)
extraction_output_entry.grid(row=1, column=1, padx=5, pady=5)
tk.Button(extraction_tab, text="Browse", command=browse_output_extraction).grid(row=1, column=2, padx=5, pady=5)

# RGB 范围输入
tk.Label(extraction_tab, text="RGB range (r_min, g_min, b_min, r_max, g_max, b_max):").grid(
    row=2, column=0, columnspan=3, padx=5, pady=5
)
extraction_ranges_textbox = scrolledtext.ScrolledText(extraction_tab, width=70, height=10)
extraction_ranges_textbox.grid(row=3, column=0, columnspan=3, padx=5, pady=5)
# 示例数据
extraction_ranges_textbox.insert(tk.END, "110, 70, 0, 120, 80, 10\n225, 150, 0, 235, 160, 10")

# 运行按钮
tk.Button(extraction_tab, text="Run Extraction", command=run_extraction, bg="green", fg="white") \
    .grid(row=4, column=0, columnspan=3, pady=10)


# 构建第二页

# 输入文件
tk.Label(polygonization_tab, text="Input PNG file:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
polygon_input_entry = tk.Entry(polygonization_tab, width=50)
polygon_input_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(polygonization_tab, text="Browse", command=browse_input_polygon).grid(row=0, column=2, padx=5, pady=5)

# 输出文件
tk.Label(polygonization_tab, text="Output GeoJSON file:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
polygon_output_entry = tk.Entry(polygonization_tab, width=50)
polygon_output_entry.grid(row=1, column=1, padx=5, pady=5)
tk.Button(polygonization_tab, text="Browse", command=browse_output_polygon).grid(row=1, column=2, padx=5, pady=5)

# 运行按钮
tk.Button(polygonization_tab, text="Run Polygonization", command=run_polygonization, bg="green", fg="white") \
    .grid(row=2, column=0, columnspan=3, pady=10)

root.mainloop()
