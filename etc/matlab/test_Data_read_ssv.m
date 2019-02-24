
d = Data();
d = d.read_ssv('data2.ssv');

xcol = d.cols{1};
xvec = d.col_vector(xcol);
for i = 2:d.ncols
    ycol = d.cols{i};
    yvec = d.col_vector(ycol);
    plot(xvec, yvec)
    xlabel(xcol)
    ylabel(ycol)
    grid
    hold on
end
