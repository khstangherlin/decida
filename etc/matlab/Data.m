classdef Data
    %=========================================================================
    % public properties
    %=========================================================================
    properties(GetAccess = 'public', SetAccess = 'private')
        ncols = 0;
        nrows = 0;
        cols = {};
    end
    %=========================================================================
    % private properties
    %=========================================================================
    properties(GetAccess = 'private', SetAccess = 'private')
        data = [];
    end
    %=========================================================================
    % private methods
    %=========================================================================
    methods(Access = 'private')
        function index = col_index(obj, col)
            index = -1;
            for i=1:obj.ncols
                if strcmp(col, obj.cols{i}) == 1
                    index = i;
                    break
                end
            end
        end
    end
    %=========================================================================
    % public methods
    %=========================================================================
    methods(Access = 'public')
        %---------------------------------------------------------------------
        % constructor
        %---------------------------------------------------------------------
        function obj = Data()
        end
        %---------------------------------------------------------------------
        % read_ssv
        %---------------------------------------------------------------------
        function obj = read_ssv(obj, file)
            fin = fopen(file,'r');
            if fin < 0
                error(['Could not open ',file,' for input']);
            end
            obj.ncols = 0;
            obj.nrows = 0;
            obj.cols = {};
            obj.data = [];
            line = fgetl(fin);
            while ischar(line)
                line = strtrim(line);     
                if length(line) == 0
                elseif line(1) == '#'
                else
                    %---------------
                    % count tokens
                    %---------------
                    obj.ncols = 0;
                    cline = line;
                    while not(isempty(cline))
                        [tok, cline] = strtok(cline);
                        obj.ncols = obj.ncols+1;
                    end
                    %--------------------
                    % cell for columns
                    %--------------------
                    obj.cols = cell(obj.ncols, 1);
                    n=0;
                    while not(isempty(line))
                        [tok, line] = strtok(line);
                        n = n+1;
                        obj.cols{n} = tok;
                    end
                    break
                end
                line = fgetl(fin);
            end
            obj.data  = fscanf(fin,'%f');
            ndata = length(obj.data);
            obj.nrows = ndata/obj.ncols;
            if obj.nrows ~= round(ndata/obj.ncols)
                fprintf(1,'\ndata: nrow = %f\tncol = %d\n', obj.nrows, obj.ncols);
                fprintf(1,'(number of data points = %d) != (nrows * ncols)\n',ndata);
                error('data is not rectangular')
            end
            %  notice the transpose operator
            obj.data = reshape(obj.data, obj.ncols, obj.nrows)'; 
        end
        %---------------------------------------------------------------------
        % col_vector
        %---------------------------------------------------------------------
        function  v = col_vector(obj, col)
            index = obj.col_index(col);
            if index > 0
                v = obj.data(:,index);
            else
                v = [];
                error('no column named %s\n', col);
            end
        end
    end
end
