# Ma trận khả nghịch

**Tên gọi khác:** khả nghịch (invertible), không suy biến (nonsingular)

Trong đại số tuyến tính, một ma trận vuông được gọi là **khả nghịch** (hoặc **đảo ngược được**) nếu tồn tại một ma trận khác sao cho khi nhân hai ma trận này với nhau, ta thu được ma trận đơn vị. Ma trận đơn vị là ma trận vuông có các phần tử trên đường chéo chính bằng 1 và các phần tử khác bằng 0.

Cụ thể, một ma trận vuông $A$ được gọi là khả nghịch nếu tồn tại ma trận $B$ sao cho:

$$AB = BA = I$$

trong đó $I$ là ma trận đơn vị cùng kích thước với $A$. 

Ví dụ, ma trận sau đây là khả nghịch:

$$A = \begin{bmatrix} 2 & 1 \\ 5 & 3 \end{bmatrix}$$

Ma trận nghịch đảo của $A$ là:

$$A^{-1} = \begin{bmatrix} 3 & -1 \\ -5 & 2 \end{bmatrix}$$

Vì khi nhân $A$ với $A^{-1}$ ta có:

$$AA^{-1} = A^{-1}A = I = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix}$$  

# Ma trận không khả nghịch

**Tên gọi khác:** suy biến (singular), không đảo ngược được (non-invertible)

Ma trận không khả nghịch là ma trận vuông không có ma trận nghịch đảo. Điều này xảy ra khi các hàng (hoặc cột) của ma trận phụ thuộc tuyến tính lẫn nhau. 

### Ví dụ ma trận không khả nghịch

$$B = \begin{bmatrix} 1 & 2 \\ 2 & 4 \end{bmatrix}$$

Ma trận này không khả nghịch vì hàng thứ hai là 2 lần hàng thứ nhất, tức là các hàng phụ thuộc tuyến tính.
