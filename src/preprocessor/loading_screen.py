# # IMPORT STATEMENTS
# import matplotlib.pyplot as plt
#
# with open("GO.dat") as file:
#     x = []
#     y = []
#     for line in file:
#         try:
#             x.append(float(line[:line.index('\t')].strip()))
#             y.append(float(line[line.index('\t') + 1:].strip()))
#         except:
#             continue
#
# x = x[-4000:]
# y = y[-4000:]
#
# # # plt.plot(x, y)
# # plt.show()
#
#
# for i in range(len(x)):
#     ax = plt.axes()
#     ax.set_facecolor("#3d4855")
#     # if (i % 2 == 0):
#     plt.plot(x, y, color="#77b5d9")
#     plt.xlim(-133, 133)
#     plt.ylim(-2, 2)
#     point_x = x[i]
#     point_y = y[i]
#     plt.scatter(point_x, point_y, color="#77b5d9")
#     plt.pause(0.001)
#     plt.clf()
#
# plt.show()

